from django.conf.urls import patterns, include, url

from url.views import spider_url,control_spider_url,spider_url_all
from article.views import spider_article,control_spider_article,spider_article_all


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'spider.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^spider_url/',spider_url),
    url(r'^control_spider_url/',control_spider_url),
    url(r'^spider_url_all/',spider_url_all),

    url(r'^spider_article/',spider_article),
    url(r'^control_spider_article/',control_spider_article),
    url(r'^spider_article_all/',spider_article_all),

)
