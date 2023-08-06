# TypeRacerScraper
Given a username and quantity of scores. Will scrape and return a CSV of scores in type racer.


from typeracerScraper_package import typeracerScraper as t

df = t.TypeRacerScraper("not_not_mk", "1000").result_dataframe()

print(df)
