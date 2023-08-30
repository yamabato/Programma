RELEASE_LOG_HTML_PATH = "/home/programming/mysite/data/release_log.html"
FEATURE_PLAN_HTML_PATH = "/home/programming/mysite/data/feature_plan.html"

def get_release_log():
    release_log_html = ""
    with open(RELEASE_LOG_HTML_PATH, mode="r") as f:
        release_log_html = f.read()

    return release_log_html

def get_feature_plan():
    feature_plan_html = ""
    with open(FEATURE_PLAN_HTML_PATH, mode="r") as f:
        feature_plan_html = f.read()

    return feature_plan_html