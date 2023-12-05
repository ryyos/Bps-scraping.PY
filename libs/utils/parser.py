from pyquery import PyQuery

class HtmlParser:
    def __init__(self) -> None:
        pass

    def parse_html(self, html: PyQuery, selector: str) -> PyQuery:
        result = None
        try:
            html: str = PyQuery(html)
            result = html.find(selector)
        except Exception as err:
            print(err)

        finally:
            return result