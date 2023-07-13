import os
import json
import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account.json'

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

property_id = "371498975"
excluded_pages = ['OKLMS: Log in to the site', 'Dashboard', 'New account', 'Confirm your account']

# Using a default constructor instructs the client to use the credentials
# specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
client = BetaAnalyticsDataClient()

request = RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[
        Dimension(name="browser"), # working
        Dimension(name="city"), 
        Dimension(name="platformDeviceCategory"), # working
        Dimension(name="deviceModel"), # working
        Dimension(name="fileName"), # working
        Dimension(name="fileExtension"), # working
        # Dimension(name="fullPageUrl"),
        Dimension(name="pageTitle"), # working
        Dimension(name="linkText"), # working
        Dimension(name="linkUrl"), # working
        ],
    metrics=[
        Metric(name="activeUsers"),
        Metric(name="averageSessionDuration"),
        Metric(name="bounceRate"),
        Metric(name="engagedSessions"),
        Metric(name="engagementRate"),
        # Metric(name="linkUrl"),  NOT WORKING
        Metric(name="newUsers"),
        Metric(name="screenPageViewsPerUser"),
        Metric(name="sessionConversionRate"),
        Metric(name="sessions"),
        Metric(name="sessionsPerUser"),
        # Metric(name="userEngagementDuration"),
        ],
    date_ranges=[DateRange(start_date="yesterday", end_date="today")],
)
response = client.run_report(request)
request1 = RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[
        Dimension(name="pageTitle"),
        Dimension(name="newVsReturning"),
        Dimension(name="outbound"),
        Dimension(name="searchTerm"),
        Dimension(name="videoProvider"),
        Dimension(name="videoTitle"),
        Dimension(name="contentGroup"),
        Dimension(name="contentId"),
        Dimension(name="contentType")
    ],
    metrics = [
        Metric(name="screenPageViews"),
        Metric(name="userEngagementDuration"),
        # Metric(name="organicGoogleSearchAveragePosition"),
        # Metric(name="organicGoogleSearchClicks"),
        # Metric(name="organicGoogleSearchClickThroughRate"),
        # Metric(name="organicGoogleSearchImpressions"),
        Metric(name="scrolledUsers"),
        Metric(name="screenPageViewsPerSession")
    ],
    date_ranges=[DateRange(start_date="yesterday", end_date="today")],
)
response1 = client.run_report(request1)

request2 = RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[
        Dimension(name="pageTitle"),
        Dimension(name="hostName"),
        Dimension(name="landingPagePlusQueryString"),
        # Dimension(name="pageLocation"),
        # Dimension(name="pagePathPlusQueryString"),
        Dimension(name="dateHour"),
        Dimension(name="operatingSystemWithVersion"),
        Dimension(name="screenResolution"),
        Dimension(name="dayOfWeekName")
    ],
    metrics = [
    ],
    date_ranges=[DateRange(start_date="yesterday", end_date="today")],
)
response2 = client.run_report(request2)

# print(response.dimension_headers[1])

# print("Report result:")
result = []

for row in response.rows:
    temp = {}
    for index, dimension in enumerate(row.dimension_values):
        temp[response.dimension_headers[index].name] = dimension.value
        
    for index, metric in enumerate(row.metric_values):
        temp[response.metric_headers[index].name] = metric.value
            
    result.append(temp)

for row in response1.rows:
    res = next((sub for sub in result if sub['pageTitle'] == row.dimension_values[0].value), None)
    for index, dimension in enumerate(row.dimension_values):
        if index != 0:
            res[response1.dimension_headers[index].name] = dimension.value
            
    for index, metric in enumerate(row.metric_values):
        res[response1.metric_headers[index].name] = metric.value

for row in response2.rows:
    res = next((sub for sub in result if sub['pageTitle'] == row.dimension_values[0].value), None)
    for index, dimension in enumerate(row.dimension_values):
        if index != 0:
            res[response2.dimension_headers[index].name] = dimension.value

with open("data/results.json", "w") as f:
    f.write(json.dumps(result, indent=4))
    
result_json = pd.read_json("data/results.json")

result_json.to_excel("data/results.xlsx")