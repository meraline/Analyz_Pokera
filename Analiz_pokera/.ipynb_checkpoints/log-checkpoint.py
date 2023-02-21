import sentry_sdk
sentry_sdk.init(
    dsn="https://440378f295354f0fadbd14a96a9614d6@o4504649572941824.ingest.sentry.io/4504649575694336",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)



division_by_zero = 1 / 0
