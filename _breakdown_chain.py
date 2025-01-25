import pandas as pd
import tldextract

def CreateOutput(data,type):
    output_csv = 'output/chains/'+type+'.csv'
    output_html = 'output/chains/'+type+'.html'
    data.to_csv(output_csv,index=False)
    json_data = data.to_json(orient='records')
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Data Flow - {type}</title>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    </head>
    <body>
        <div id="sankey_multiple"></div>

        <script type="text/javascript">
            google.charts.load("current", {{packages:["sankey"]}});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {{
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'source');
                data.addColumn('string', 'target');
                data.addColumn('number', 'value');

                var jsonData = {json_data};
                jsonData.forEach(function(row) {{
                    data.addRow([row.source, row.target, row.value]);
                }});

                var colors = ['#37a2fe', '#37a2fe', '#37a2fe', '#37a2fe', '#37a2fe', '#37a2fe', '#37a2fe', '#37a2fe', '#37a2fe'];

                
                var options = {{
                    height: 8000,
                    sankey: {{
                        node: {{
                            label: {{
                                fontName: 'Helvetica',
                                fontSize: 9,
                                color: '#871b47',
                                bold: true
                            }},
                            nodePadding: 10
                        }}
                    }},
                }};

                var chart = new google.visualization.Sankey(document.getElementById('sankey_multiple'));
                chart.draw(data, options);
            }}
        </script>
    </body>
    </html>
    """
    # Create and write to the HTML file
    with open(output_html, 'w') as file:
        file.write(html_content)

    print(type+" - CSV file stored at "+output_csv)
    print(type+" - HTML file stored at "+output_html)

def Visualize(type):
    data_raw = pd.read_csv('input/Adhoc/Japan/'+type+'.csv.gz',compression='gzip')
    data = RunData(data_raw)
    CreateOutput(data,type)
    
def RunData(df):
    st = []
    init = []
    rd = []

    for index, row in df.iterrows():
        st.append(row['st_domain'])
        if(pd.isna(row['initiator_url']) == False):
            init_domain = tldextract.extract(row['initiator_url']).registered_domain
            
            if ((init_domain != row['thrd_domain']) and (init_domain != row['st_domain'])):
                init.append(init_domain)
            else:
                init.append('')
        else:
            init.append('')
        rd.append(row['thrd_domain'])

    dict_trace = {'st_domain':st,'initiator':init,'thrd_domain':rd}
    df_trace = pd.DataFrame(dict_trace)
    df_trace = df_trace.drop_duplicates()
    
    source = []
    target = []
    value = []
    
    for index,row in df_trace.iterrows():
        if row['initiator'] != '':
            source.append(row['st_domain'])
            target.append(row['initiator'])
            value.append(1)
            
            source.append(row['initiator'])
            target.append(row['thrd_domain'])
            value.append(1)
        
        else:
            source.append(row['st_domain'])
            target.append(row['thrd_domain'])
            value.append(1)
    
    dict_chart = {'source':source,'target':target,'value':value}
    df_chart = pd.DataFrame(dict_chart)
    list_trace_org = df_chart.values.tolist()
    
    value_st_init = 0
    value_init_rd = 0
    
    value_st_rd = 0
    
    for l in list_trace_org:
        if l == ['st_domain','initiator']:
            value_st_init += 1
        if l == ['initiator','thrd_domain']:
            value_init_rd += 1
        if l == ['st_domain','thrd_domain']:
            value_st_rd += 1

    cycles = set()
    for index, row in df_chart.iterrows():
        if (row['target'], row['source']) in cycles:
            df_chart = df_chart[~((df_chart['source'] == row['target']) & (df_chart['target'] == row['source']))]
        else:
            cycles.add((row['source'], row['target']))
    
    return df_chart
    
types = ["Google","Facebook"]
for t in types:
    Visualize(t)