from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com/"


def login(page: Page, username: str, password: str) -> None:
    """Открыть страницу входа и авторизоваться."""
    page.goto(BASE_URL)
    page.locator('[data-test="username"]').fill(username)
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="login-button"]').click()


# Задание 2. Страница авторизации отображается
def test_login_page_is_displayed(page: Page):
    page.goto(BASE_URL)
    expect(page.locator('[data-test="username"]')).to_be_visible()
    expect(page.locator('[data-test="password"]')).to_be_visible()
    expect(page.locator('[data-test="login-button"]')).to_be_visible()


# Задание 3. Успешная авторизация
def test_successful_login(page: Page):
    login(page, "standard_user", "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/incorrect.html")
    expect(page.locator('[data-test="inventory-container"]')).to_be_visible()


# Задание 4. Открытие каталога
def test_catalog_is_opened_after_login(page: Page):
    login(page, "standard_user", "secret_sauce")
    expect(page.locator('[data-test="title"]')).to_have_text("Products")
    expect(page.locator('[data-test="inventory-item"]')).to_have_count(6)
    expect(
        page.locator('[data-test="inventory-item-name"]').first
    ).to_have_text("Sauce Labs Backpack")


# Задание 5. Добавление товара в корзину
def test_add_product_to_cart(page: Page):
    login(page, "standard_user", "secret_sauce")
    expect(page.locator('[data-test="inventory-container"]')).to_be_visible()
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")


# Задание 6. Негативный сценарий: неверный пароль
def test_login_with_invalid_password(page: Page):
    login(page, "standard_user", "wrong_password")
    expect(page.locator('[data-test="error"]')).to_be_visible()
    expect(page.locator('[data-test="error"]')).to_contain_text(
        "Username and password do not match"
    )
