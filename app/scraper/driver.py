from selenium import webdriver


def creer_driver():
    """Crée et configure le navigateur Chrome."""

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Réduit certains messages liés à l'automatisation.
    options.add_experimental_option(
        "excludeSwitches",
        ["enable-automation"]
    )

    driver = webdriver.Chrome(options=options)

    return driver