import sqlite3
import plotly.plotly as py
import plotly.graph_objs as go

stat_list = ["total","hp","attack","defense","specialattack","specialdefense","speed"]
char_list = stat_list + ["height","weight"]
type_list = ["Normal","Fire","Fighting","Water","Flying","Grass","Poison","Electric","Ground","Psychic",
            "Rock","Ice","Bug","Dragon","Ghost","Dark","Steel","Fairy"]

class Condition:
    def __init__(self,st):
        self.stat = None
        self.con = None
        self.num = None
        self.val = False
        for con in [">","=","<"]:
            try:
                v2 = False
                s = st.split(con)
                for stat in stat_list:
                    if stat == s[0]:
                        v2 = True
                i = float(s[1])
                if v2:
                    self.stat = s[0]
                    self.con = con
                    self.num = i
                    self.val = True
            except:
                pass
    def __str__(self):
        return("{0.stat}{0.con}{0.num}".format(self))
        
def check_type(st):
    valid = False
    for t in type_list:
        if t.lower()==st:
            valid = True
    return(valid)

def top_bottom_clause(com,t_b):
    lim_comm = "LIMIT(10)"
    if t_b == 't':
        try:
            lim = int(com.split("=")[1])
            lim_comm = "LIMIT({})".format(str(lim))
        except:
            print('Error. Proper format is "top=<limit>"')
    else:
        try:
            lim = int(com.split("=")[1])
            lim_comm = "LIMIT({})".format(str(lim))
        except:
            print('Error. Proper format is "bottom=<limit>"')
    return(lim_comm)

def bar_command(command):
    where_comm = None
    join_comm = "JOIN Stats ON Pokemon.Name=Stats.PokemonName "
    groupby_comm = "GROUP BY Type1 "
    order_comm = "ORDER BY Rating "
    dir_comm = "DESC "
    lim_comm = "LIMIT(5)"

    if len(command)<=4:
        valid = True
        for com in command:
            lst = ["cond:","stat=","top=","bottom="]
            if (com not in ["bar","scatter","box","hist"]) and not any(x in com for x in lst):
                valid = False

        if valid:
            val_stat = None
            val_where = True
            for com in command:
                if "cond:" in com:
                    s = Condition(com.split(":")[1])
                    if s.val:
                        where_comm = "WHERE {}{}{} ".format(s.stat,s.con,s.num)
                    else:
                        print('Error. Proper format is "cond:<stat>{>,=,<}<number>"')
                        val_where = False
                
                c = com.split("=")
                if "stat" == c[0] and len(c)==2:
                    if c[1] in stat_list:
                        sel_comm = "SELECT Type1, ROUND(AVG({}),2) ".format(c[1])
                        order_comm = "ORDER BY AVG({}) ".format(c[1])
                        val_stat = c[1].capitalize()

                if "top=" in com:
                    lim_comm = top_bottom_clause(com,'t')
                elif "bottom=" in com:
                    dir_comm = "ASC "
                    lim_comm = top_bottom_clause(com,'b')

            if val_stat is not None:
                if val_where:
                    sql_comm = sel_comm + "FROM Pokemon " + join_comm 

                    if where_comm is not None:
                        sql_comm += where_comm

                    sql_comm += groupby_comm + order_comm + dir_comm + lim_comm

                    return(sql_comm,val_stat)
            else:
                print('Error. Requires "stat=<metric>"')
        
        else:
            print("Command not recognized: {}".format(' '.join(command)))
            return(None)

    else:
        print("Error. Bar only takes three parameters.")
        return(None)

def scatter_command(command):
    where_comm = None
    join_comm = "JOIN Stats ON Pokemon.Name=Stats.PokemonName "
    types_chosen = []

    if len(command)<=3:
        valid = True
        for com in command:
            lst = ["type=","stat="]
            if (com not in ["bar","scatter","box","hist"]) and not any(x in com for x in lst):
                valid = False

        if valid:
            val_stat = None
            val_where = True
            for com in command:
                if "type=" in com:
                    s = com.split("=")
                    cs = s[1].split(",")
                    
                    where_comm = "WHERE "
                    for ty in cs:
                        
                        if check_type(ty):
                            where_comm += "Type1='{0}' OR Type2='{0}' OR ".format(ty.capitalize())
                            types_chosen.append(ty.capitalize())
                        elif ty=="all":
                            types_chosen = type_list[:]
                            where_comm = where_comm[:-3]
                        else:
                            val_where = False
                    where_comm = where_comm[:-4]
                    if not val_where:
                        print('Error. Proper format is "type=<type>,<type>..."')
                
                c = com.split("=")
                if "stat" == c[0] and len(c)==2:
                    if c[1] in stat_list:
                        sel_comm = "SELECT Name, {}, Type1, Type2, Id ".format(c[1])
                        val_stat = c[1].capitalize()

            if val_stat is not None:
                if val_where:
                    sql_comm = sel_comm + "FROM Pokemon " + join_comm 

                    if where_comm is not None:
                        sql_comm += where_comm



                    return(sql_comm,[types_chosen,val_stat])
            else:
                print('Error. Requires "stat=<metric>"')
                return(None)
        
        else:
            print("Command not recognized: {}".format(' '.join(command)))
            return(None)

    else:
        print("Error. Scatter only takes two parameters.")
        return(None)

def histogram_command(command):
    sel_comm = "SELECT Height "
    where_comm = None
    join_comm = "JOIN Stats ON Pokemon.Name=Stats.PokemonName "
    type_chosen = None
    density = False
    metric = "Heights"

    if len(command)<=4:
        valid = True
        for com in command:
            lst = ["type="]
            if (com not in ["bar","scatter","box","hist","height","weight","density","count"]) and not any(x in com for x in lst):
                valid = False

        if valid:
            val_where = True
            for com in command:
                if "type=" in com:
                    s = com.split("=")
                    if check_type(s[1]):
                        where_comm = "WHERE Type1='{0}' OR Type2='{0}' ".format(s[1].capitalize())
                        type_chosen = s[1].capitalize()
                    else:
                        print('Error. Proper format is "type=<type>"')
                        val_where = False
                
                if com == "weight":
                    sel_comm = "SELECT Weight "
                    metric = "Weights"

                if com == "density":
                    density = True

            if val_where:
                sql_comm = sel_comm + "FROM Pokemon " + join_comm 

                if where_comm is not None:
                    sql_comm += where_comm

                return(sql_comm,[type_chosen,density,metric])
        
        else:
            print("Command not recognized: {}".format(' '.join(command)))
            return(None)

    else:
        print("Error. Hist only takes three parameters.")
        return(None)

def boxplot_command(command):
    where_comm = None
    join_comm = "JOIN Stats ON Pokemon.Name=Stats.PokemonName "
    types_chosen = []
    metric = None

    if len(command)<=3:
        valid = True
        for com in command:
            lst = ["type=","stat="]
            if (com not in ["bar","scatter","box","hist"]) and not any(x in com for x in lst):
                valid = False

        if valid:
            val_stat = False
            val_where = True
            for com in command:
                if "type=" in com:
                    s = com.split("=")
                    cs = s[1].split(",")
                    
                    where_comm = "WHERE "
                    for ty in cs:
                        
                        if check_type(ty):
                            where_comm += "Type1='{0}' OR Type2='{0}' OR ".format(ty.capitalize())
                            types_chosen.append(ty.capitalize())
                        elif ty=="all":
                            types_chosen = type_list[:]
                            where_comm = where_comm[:-3]
                        else:
                            val_where = False
                    where_comm = where_comm[:-4]
                    if not val_where:
                        print('Error. Proper format is "type=<type>,<type>..."')

                
                c = com.split("=")
                if "stat" == c[0] and len(c)==2:
                    if c[1] in char_list:
                        sel_comm = "SELECT {}, Type1, Type2 ".format(c[1])
                        metric = c[1].capitalize()
                        val_stat = True

            if val_stat:
                if val_where:
                    sql_comm = sel_comm + "FROM Pokemon " + join_comm 

                    if where_comm is not None:
                        sql_comm += where_comm
                    return(sql_comm,[types_chosen,metric])
            else:
                print('Error. Requires "stat=<metric>"')
                return(None)
        
        else:
            print("Command not recognized: {}".format(' '.join(command)))
            return(None)

    else:
        print("Error. Box only takes two parameters.")
        return(None)

def process_command(command):
    command = command.split()
    keyword = command[0].lower()
    sql_comm = None
    extras = None
    
    if keyword == 'bar':
        bar_c = bar_command(command)
        if bar_c is not None:
            sql_comm = bar_c[0]
            extras = bar_c[1]
    elif keyword == 'scatter':
        scatter_c = scatter_command(command)
        if scatter_c is not None:
            sql_comm = scatter_c[0] 
            extras = scatter_c[1]
    elif keyword == 'hist':
        hist_c = histogram_command(command)
        if hist_c is not None:
            sql_comm = hist_c[0]
            extras = hist_c[1]
    elif keyword == 'box':
        box_c = boxplot_command(command)
        if box_c is not None:
            sql_comm = box_c[0]
            extras = box_c[1]

    c = []
    if sql_comm is not None:
        conn = sqlite3.connect('pokemon.db')
        cur = conn.cursor()
        c = cur.execute(sql_comm).fetchall()
    else:
        c = None

    return(c,keyword,extras)


def type_colors(t):
    col_list = ["rgb(255,160,122)","rgb(255,0,0)","rgb(128,0,0)","rgb(0,0,255)","rgb(0,255,127)","rgb(34,139,34)","rgb(75,0,130)","rgb(255,255,0)","rgb(160,82,45)",
            "rgb(128,0,128)","rgb(139,69,19)","rgb(0,191,255)","rgb(124,252,0)","rgb(255,69,0)","rgb(147,112,219)","rgb(0,0,0)","rgb(112,138,144)","rgb(255,0,255)"]

    for i in range(len(type_list)):
        if t == type_list[i]:
            return(col_list[i])

def barplot(data,extra):
    x,y,color_list=[],[],[]
    for row in data:
        x.append(row[0])
        y.append(row[1])
        color_list.append(type_colors(row[0]))
    d = [go.Bar(x=x,y=y,marker=dict(color=color_list),text=x)]
    
    layout = go.Layout(title='Barplot of {} by Type'.format(extra))
    fig = go.Figure(data=d, layout=layout)
    return(fig)

def scatterplot(data,extra):
    if len(extra[0])>0:
        d = []
        for t in extra[0]:
            x,y,name_list=[],[],[]
            for row in data:
                if row[2]==t or row[3]==t:
                    x.append(row[4])
                    y.append(row[1])
                    name_list.append(row[0])
            color = type_colors(t)

            trace = go.Scatter(x=x,y=y,name=t,mode = 'markers',marker = dict(size=10,color=color),text=name_list)
            d.append(trace)

        layout = dict(title = 'Scatterplot of {}'.format(extra[1]))
        fig = dict(data=d, layout=layout)
    else:
        x,y,name_list=[],[],[]
        for row in data:
            x.append(row[4])
            y.append(row[1])
            name_list.append(row[0])

        trace = go.Scatter(x=x,y=y,name="All",mode = 'markers',marker = dict(size=10),text=name_list)

        layout = dict(title = 'Scatterplot of {}'.format(extra[1]))
        fig = dict(data=[trace], layout=layout)
    return(fig)

def densityplot(data,extra):
    x = []
    for row in data:
        x.append(row[0])

    if extra[1]:
        if extra[0] is not None:
            d = [go.Histogram(x=x,histnorm='probability',marker=dict(color=type_colors(extra[0])))]
            descriptive = " {}".format(extra[0])
        else:
            d = [go.Histogram(x=x,histnorm='probability')]
            descriptive = ""
        layout = dict(title = 'Normalized Histogram of{} Pokemon {}'.format(descriptive,extra[2]))
        fig = dict(data=d, layout=layout)
        return(fig)
    else:
        if extra[0] is not None:
            d = [go.Histogram(x=x,marker=dict(color=type_colors(extra[0])))]
            descriptive = " {}".format(extra[0])
        else:
            d = [go.Histogram(x=x)]
            descriptive = ""
        layout = dict(title = 'Histogram of{} Pokemon {}'.format(descriptive,extra[2]))
        fig = dict(data=d, layout=layout)
        return(fig)

def boxplot(data,extra):
    if len(extra[0])>0:
        d = []
        for t in extra[0]:
            y = []
            for row in data:
                if row[1]==t or row[2]==t:
                    y.append(row[0])
            color = type_colors(t)

            trace = go.Box(y=y,name=t,marker = dict(color=color))
            d.append(trace)

        layout = dict(title = 'Pokemon {} Boxplot'.format(extra[1]))
        fig = dict(data=d, layout=layout)
    else:
        y = []
        for row in data:
            y.append(row[0])

        trace = go.Box(y=y,name="All")

        layout = dict(title = 'Pokemon {} Boxplot'.format(extra[1]))
        fig = dict(data=[trace], layout=layout)
    return(fig)

def plot(data,plot_type,extra=None):
    if len(data)>0:
        if plot_type == "bar":
            fig = barplot(data,extra)
            py.plot(fig, filename='barplot')
        elif plot_type == "scatter":
            fig = scatterplot(data,extra)
            py.plot(fig, filename='scatter')
        elif plot_type == "hist":
            fig = densityplot(data,extra)
            py.plot(fig, filename='histogram')
        elif plot_type == "box":
            fig = boxplot(data,extra)
            py.plot(fig, filename='boxplot')
    else:
        print("No data to plot!")

def interactive_prompt():
    help_text = '''\nBarplot:\n    REQUIRES: bar stat=<stat>\n    OPTION: cond:<stat>[>,=,<]<number> top=<limit> bottom=<limit>\nBoxplot:\n\
    REQUIRES: box stat=<metric>\n    OPTION: type=<type>,<type>,<type>.. or type=all\nHistogram:\n    REQUIRES: hist\n    DEFAULT: height count\n\
    OPTION: type=<type> weight density\nScatterplot:\n    REQUIRES: scatter stat=<stat>\n    OPTION type=<type>,<type>,<type>.. or type=all\n\nTYPE LIST: {0}\n\
    \nSTAT LIST: {1}\n\nMETRIC LIST: stat list + height and weight\n\nType "exit" to end program.'''.format(", ".join(sorted(type_list)),", ".join(sorted(stat_list)))
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')
        try:
            r = response.split()[0].lower()
        except:
            r = ""

        if r == 'help':
            print(help_text)
        elif r == 'exit' or r == "":
            pass
        elif r == "bar":
            b = process_command(response)
            if b[0] is not None:
                print("Plotting barplot...")
                plot(*b)
        elif r == "scatter":
            s = process_command(response)
            if s[0] is not None:
                print("Plotting scatterplot...")
                plot(*s)
        elif r == "hist":
            h = process_command(response)
            if h[0] is not None:
                print("Plotting histogram...")
                plot(*h)
        elif r == "box":
            b = process_command(response)
            if b[0] is not None:
                print("Plotting boxplot...")
                plot(*b)
        else:
            print('Command not recognized: {} \nType "help" for more options.'.format(response))

        print("")

if __name__=="__main__":
    interactive_prompt()