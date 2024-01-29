import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class plot:
    def blast(self):
        data = pd.read_table('all_combinetable', header=None)     #path to chmbinetable
        data.columns = ["gene_query", "chr_query","san", "start_query", "end_query", "strand_query",
                        "gene_ref", "chr_ref","jiu", "start_ref", "end_ref", "strand_ref", "score"]
        data['strand'] = '+'
        data.loc[data['strand_query'] != data['strand_ref'], 'strand'] = '-'

        data = data[data['chr_query'].astype(str).isin(
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])]
        data = data[data['chr_ref'].astype(str).isin(
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])]
        data['chr_query'] = pd.Categorical(data['chr_query'],categories=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
        data['chr_ref'] = pd.Categorical(data['chr_ref'],categories=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])

        sns.set(style="white")
        g = sns.FacetGrid(data, col='chr_query', row='chr_ref', hue='strand', height=1.5, aspect=1.5,margin_titles=True)

        '''for ax, (chr_query, chr_ref) in zip(g.axes.flat, g.facet_data()):
            subset_data = data[(data['chr_query'] == chr_query) & (data['chr_ref'] == chr_ref)]
            if not subset_data.empty:
                subset_data = subset_data[['start_query', 'start_ref']]
                max_x_value = subset_data['start_query'].max()
                max_y_value = subset_data['start_ref'].max()
                ax.set_xticks([0, max_x_value / 2, max_x_value])
                ax.set_yticks([0, max_y_value / 2, max_y_value])'''

        g.map(sns.scatterplot, "start_query", "start_ref", s=0.5)
        g.set_axis_labels(x_var='sb',y_var='mz')
        g.set_titles(row_template="{row_name}", col_template="{col_name}")

        plt.show()



    def collinearity_plot(self):               #Need to modify
        data = pd.read_csv("zm_sb.collinearity" ,header=0, sep='\t', comment='#')
        data = data[data['queryChr'].astype(str).isin(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])]
        data = data[data['refChr'].astype(str).isin(["chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8", "chr9", "chr10"])]
        data['queryChr'] = pd.Categorical(data['queryChr'],categories=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        data['refChr'] = pd.Categorical(data['refChr'],categories=["chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8", "chr9", "chr10"])
        print(data)

        sns.set(style="white")
        g = sns.FacetGrid(data, col='refChr', row='queryChr', hue='strand', height=1.5, aspect=1.5,margin_titles=True)
        g.map(sns.scatterplot, "referenceStart", "queryStart", s=0.5)
        g.set_axis_labels(x_var='sb', y_var='mz')
        g.set_titles(row_template="{row_name}", col_template="{col_name}")

        plt.show()



plot = plot()
plot.collinearity_plot()

