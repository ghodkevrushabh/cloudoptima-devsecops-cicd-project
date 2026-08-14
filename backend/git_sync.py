def push_to_github(app_name):
    """
    Git operations are handled by Jenkins.
    Flask only generates IaC files.
    """

    print(
        f"INFO: IaC generated for {app_name}. "
        "Git push will be handled by Jenkins."
    )

    return True
