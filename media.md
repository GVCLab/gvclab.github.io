---
title: 媒体报道
layout: page
description: GVC Lab 的媒体报道、专访与研究成果解读。
permalink: "/media/"
---

<style>
  .media-coverage .media-intro {
    color: #555;
    margin-bottom: 1.8rem;
  }
  .media-coverage .media-list {
    display: grid;
    gap: 1rem;
  }
  .media-coverage .media-item,
  .media-coverage .media-empty {
    padding: 1.25rem;
    border: 1px solid #e0e0e0;
    border-left: 4px solid #e8572a;
    border-radius: 8px;
    background: #fff;
  }
  .media-coverage .media-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 1rem;
    margin-bottom: 0.6rem;
    color: #666;
    font-size: 0.875rem;
  }
  .media-coverage .media-title {
    margin: 0;
    font-size: 1.125rem;
    line-height: 1.6;
    overflow-wrap: anywhere;
  }
  .media-coverage .media-title a:focus-visible {
    outline: 2px solid #e8572a;
    outline-offset: 4px;
  }
  .media-coverage .media-summary {
    margin: 0.75rem 0 0;
    color: #555;
  }
  .media-coverage .media-related {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 1rem;
    margin: 0.75rem 0 0;
    font-size: 0.875rem;
  }
  .media-coverage .media-empty p {
    margin: 0;
    color: #666;
  }
</style>

<section class="media-coverage" lang="zh-CN" aria-label="媒体报道">
  <p class="media-intro">收录 GVC Lab、团队成员与合作研究的媒体报道、学校报道及研究成果解读。<a href="{{ '/#media-coverage' | relative_url }}">返回首页媒体报道</a></p>

  {% assign coverage = site.data.media | sort: 'date' | reverse %}
  {% if coverage.size > 0 %}
  <div class="media-list">
    {% for report in coverage %}
    <article class="media-item">
      <div class="media-meta">
        <span>{{ report.outlet | escape }}</span>
        <time datetime="{{ report.date | date: '%Y-%m-%d' }}">{{ report.date | date: '%Y-%m-%d' }}</time>
        {% if report.language == 'en' %}<span lang="en">English</span>{% elsif report.language == 'ru' %}<span>俄文</span>{% endif %}
        {% if report.category %}<span>{{ report.category | escape }}</span>{% endif %}
      </div>
      <h2 class="media-title"><a href="{{ report.url | escape }}" target="_blank" rel="noopener noreferrer" aria-label="{{ report.title | escape }}（在新标签页打开）">{{ report.title | escape }}</a></h2>
      {% if report.summary %}<p class="media-summary">{{ report.summary | escape }}</p>{% endif %}
      {% if report.related_links.size > 0 %}
      <p class="media-related">
        {% for link in report.related_links %}
        <a href="{{ link.url | escape }}" target="_blank" rel="noopener noreferrer" aria-label="{{ link.label | escape }}（在新标签页打开）">{{ link.label | escape }}</a>
        {% endfor %}
      </p>
      {% endif %}
    </article>
    {% endfor %}
  </div>
  {% else %}
  <div class="media-empty">
    <p>报道内容将陆续更新，敬请关注。</p>
  </div>
  {% endif %}
</section>
