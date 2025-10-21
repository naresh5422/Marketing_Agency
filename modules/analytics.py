#Pull performance metrics from APIs
#Calculate ROI, CTR, engagement rate, conversion rate

def calculate_roi(spend, revenue):
    if spend == 0:
        return 0
    return (revenue - spend) / spend
