# This is a simple crawler implemented by Python 3.6

## Change mongodb to other databases
The crawled pages and the pending crawl pages are saved to mongodb by default.

If you want to change to other databases, you could implement your own class inherited from `DbBase`(Default I use mongodb, so class `MongoDbQueue` is my instance.).

After you have your own `DbBase` class, add it to the variable `DB_CLASS_NAME` in file `project_settings.py`, and also you should provide your `DB_CONNECTION_STRING` and `DB_REPOSITORY_NAME` to connect to the database.


## Change html resolver of your own
In current version, only links (`<a>` tags in html) will be saved to the database. If you want to customized the behavior of the spiders, you can also implement your own `HTMLParser` class to replace `HtmlResolver` in my code. Don't forget to replace your own parser name to `HTML_RESOLVER_NAME` in file `project_settings.py`


## Make it better
I start to learn python a week ago, maybe made some stupid mistakes and have some bugs. I'll be very appreciate if you can help me to improve my code, thanks.
