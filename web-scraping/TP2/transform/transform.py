import pandas as pd

def transforms_data(quotes_citation, quotes_authors, quotes_tags):
    df_citations = pd.DataFrame(quotes_citation, columns=['Citations'])
    df_authors = pd.DataFrame(quotes_authors, columns=['Auteurs'])
    df_tags = pd.DataFrame(quotes_tags, columns=['Tags'])

    with pd.ExcelWriter('test-quotes.xlsx', engine='openpyxl') as writer:
        df_citations.to_excel(writer, sheet_name='Citations', index=False)
        df_authors.to_excel(writer, sheet_name='Auteurs', index=False)
        df_tags.to_excel(writer, sheet_name='Tags', index=False)