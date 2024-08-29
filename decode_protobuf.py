import logging
import appanalytics_pb2
from mitmproxy import contentviews
from mitmproxy import flow
from mitmproxy import http
from mitmproxy.addonmanager import Loader
from dataclasses import dataclass, field
import re


@dataclass
class MitmproxyUtils:
    ENDPOINT_ANDROID: str
    ENDPOINT_IOS: str
    VIEW_NAME: str
    VIEW_DESCRIPTION: str
    TAG: str
    _error_message: str = field(init=False, repr=False)
    _info_request_GA4: str = field(init=False, repr=False)


    def __post_init__(self) -> None:
        self._error_message = f"{self.TAG} => protobuf decoding error:"
        self._info_request_GA4 = f"{self.TAG} => a request has been made to GA4. url:"


    def improve_reading_values(self, log: str) -> str:
        """Maps the name of events, parameters and user properties according to what is exported to BigQuery.

        Args:
            log (str): string representing the request data.

        Returns:
            str: enhanced string representing the request data.
        """
        # events
        events = {"_cmp": "firebase_campaign", "_s": "session_start", "_vs": "screen_view",
                  "_e": "user_engagement", "_cd": "app_clear_data", "_ui": "app_remove", "_f": "first_open"
                  }
        # parameters
        parameters = {"_o": "firebase_event_origin", "_sc": "firebase_screen_class", "_pc": "ga_previous_class", "_pi": "ga_previous_id",
                      "_pn": "ga_previous_screen", "_sn": "firebase_screen", "_si": "firebase_screen_id", "_cis": "campaign_info_source",
                      "_c": "ga_conversion", "_mst": "manual_tracking", "_et": "engagement_time_msec", "_dbg": "debug_event",
                      "_pfo": "previous_first_open_count", "_sys": "system_app", "_uwa": "update_with_analytics", "_sysu": "system_app_update"
                      }
        # user property
        user_property = {"_fot" : "first_open_time", "_fi": "first_open_after_install", "_sno": "ga_session_number",
                         "_sid": "ga_session_id", "_lte": "lifetime_user_engagement", "_se": "session_user_engagement",
                         "_id" : "user_id", "_npa" : "non_personalized_ads"
                         }
        for name, value in events.items():
            log = re.sub(f"\"{name}\"", f"\"{value}\"", log)
        for name, value in parameters.items():
            log = re.sub(f"\"{name}\"", f"\"{value}\"", log)
        for name, value in user_property.items():
            log = re.sub(f"\"{name}\"", f"\"{value}\"", log)
        
        return log


proxy_utils = MitmproxyUtils(
    ENDPOINT_ANDROID='app-measurement.com/a',
    ENDPOINT_IOS='app-analytics-services-att.com/a',
    VIEW_NAME="protobuf to GA4",
    VIEW_DESCRIPTION="protobuf decoded to GA4",
    TAG="APP_TRACKING"
)


class ViewProtobuf(contentviews.View):
    name = proxy_utils.VIEW_NAME

    def __call__(
        self,
        data: bytes,
        *,
        content_type: str | None = None,
        flow: flow.Flow | None = None,
        http_message: http.Message | None = None,
        **unknown_metadata,
    ) -> contentviews.TViewResult:
        url = flow.request.url
        try:
            if (proxy_utils.ENDPOINT_ANDROID in url) or (proxy_utils.ENDPOINT_IOS in url):
                batch = appanalytics_pb2.Batch()
                batch.ParseFromString(data)
                data_string = repr(batch)
                return proxy_utils.VIEW_DESCRIPTION, contentviews.format_text(proxy_utils.improve_reading_values(data_string))
            
        except Exception as e:
            logging.info(f"{proxy_utils._error_message} {e}")
            

    def render_priority(
        self,
        data: bytes,
        *,
        content_type: str | None = None,
        flow: flow.Flow | None = None,
        http_message: http.Message | None = None,
        **unknown_metadata,
    ) -> float:
        url = flow.request.url
        if (proxy_utils.ENDPOINT_ANDROID in url) or (proxy_utils.ENDPOINT_IOS in url):
            return 1
        else:
            return 0


view = ViewProtobuf()


def load(loader: Loader):
    contentviews.add(view)


def done():
    contentviews.remove(view)


def request(flow):
    url = str(flow.request.url)
    if (proxy_utils.ENDPOINT_ANDROID in url) or (proxy_utils.ENDPOINT_IOS in url):
        logging.info(f"{proxy_utils._info_request_GA4} {url}")
