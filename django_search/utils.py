import matplotlib.pyplot as plt
import base64
from io import BytesIO

def get_graph():
    buffer=BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png=buffer.getvalue()
    graph=base64.b64encode(image_png)
    graph= graph.decode('utf-8')
    buffer.close()
    return graph

def get_bargraph(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title('Grade vs Count')
    plt.bar(x,y ,color ='maroon',
        width = 0.4)
    plt.xlabel('Grade')
    plt.ylabel('Count')
    plt.show()
    plt.tight_layout()
    graph= get_graph()
    return graph


def get_piegraph(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title('Variety vs Percentage')
    plt.xlabel('variety')
    plt.ylabel('percentage')
    plt.bar(x,y)
    plt.show()
    plt.tight_layout()
    graph= get_graph()
    return graph

def get_plot(x,y,variety):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title('Date vs Modal Price')
    for i in range(len(y.columns)):
        plt.plot(x,y.iloc[:,i])
    plt.legend(variety)
    plt.xlabel('Date')
    plt.ylabel('Modal Price')
    plt.xticks(rotation=90)
    plt.show()
    plt.tight_layout()
    graph= get_graph()
    return graph
