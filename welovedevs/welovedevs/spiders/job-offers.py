import scrapy

class JobSpider(scrapy.Spider):
    name = 'job_spider'
    allowed_domains = ['welovedevs.com']
    start_urls = ['https://welovedevs.com/app/jobs?query=&page=1']

    def parse(self, response):
        # Extract job offer links
        job_links = response.css('a.contents::attr(href)').extract()

        for job_link in job_links:
            # Build the full URL for each job offer
            full_job_link = response.urljoin(job_link)

            # Follow the link to the job offer page and call parse_job_details method
            yield scrapy.Request(url=full_job_link, callback=self.parse_job_details)

        # Increment page number and generate the next URL
        current_page = int(response.url.split('=')[-1])
        next_page = current_page + 1
        next_url = f'https://welovedevs.com/app/jobs?query=&page={next_page}'

        # Check if there are more pages to scrape
        if next_page <= 19:
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_job_details(self, response):
        # Extract detailed information from the job offer page
        job_title = response.css('h1::text').get()
        featured = response.css('.ds-inline-flex span::text').get()
        experience = response.css('span.ds-flex.ds-items-center[style="color:#3830a3"]::text').get()
        job_description_paragraphs = response.css('span.ds-font-w3d.prose p::text').extract()

        # Concatenate paragraphs to create the job description and remove '\n' characters
        job_description = ' '.join(job_description_paragraphs).replace('\n', '')

        # Yield the complete job details
        yield {
            'job_title': job_title,
            'featured': featured,
            'experience': experience,
            'job_description': job_description,
        }
