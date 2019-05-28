''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''

from helpers import *
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.embed import server_document
from bokeh.server.server import Server


# Initial values
INIT_M1 = 10 # mass object 1
INIT_M2 = 20 # mass object 1
INIT_D = 1 # distance
INIT_I = 0 # inclination
INIT_F = 40 # frequency
INIT_PHI0 = 0 # phi_zero

def modify_doc(doc):

    # Set up data
    x = tDomain(INIT_M1, INIT_M2, INIT_F)
    yPlus = hPlus(x, INIT_M1, INIT_M2, INIT_D, INIT_I, INIT_F, INIT_PHI0)
    yCross = hCross(x, INIT_M1, INIT_M2, INIT_D, INIT_I, INIT_F, INIT_PHI0)
    initTcoal = calcTcoal(INIT_M1, INIT_M2, INIT_F)
    initHmax = hMax(INIT_M1, INIT_M2, INIT_D, INIT_I, INIT_F, INIT_PHI0)
    sourcePlus = ColumnDataSource(data=dict(x=x-initTcoal, y=yPlus))
    sourceCross = ColumnDataSource(data=dict(x=x-initTcoal, y=yCross))

    # Set up plot
    plot = figure(plot_height=400, plot_width=800, title="Polarization amplitude binary",
                  tools="crosshair,pan,reset,save,wheel_zoom",
                  x_range=[-initTcoal*1.05, initTcoal*.05], y_range=[-initHmax, initHmax], logo=None)
    plot.line('x', 'y', source=sourcePlus, line_width=1, line_alpha=1, legend="h-plus (h+)")
    plot.line('x', 'y', source=sourceCross, line_color="orange", line_width=1, line_alpha=1, legend="h-cross (hx)")

    # Add labels and legend
    plot.xaxis.axis_label = "Time [s]"
    plot.yaxis.axis_label = "Strain"
    plot.legend.location = 'top_left'

    # Add vertical line
    coal = Span(location=0, dimension='height', line_color='red', line_dash="dotted", line_width=1)
    plot.add_layout(coal)

    # Set up widgets
    mass1 = Slider(title="Mass 1", value=10, start=8, end=80, step=1)
    mass2 = Slider(title="Mass 2", value=20, start=8, end=80, step=1)
    distance = Slider(title="Distance (Mpc)", value=1, start=1, end=100, step=.1)
    inclination = Slider(title="Inclination", value=0, start=0, end=2*np.pi, step=.1)
    frequency = Slider(title="Frequency (Hz)", value=40, start=1, end=100, step=.1)
    phi_zero = Slider(title="Phi_0", value=0, start=0, end=np.pi/2, step=.1)

    # Function that updates all parameters when sliders are changed
    def update_data(attr, old, new):

        # Get the current slider values
        m1 = mass1.value
        m2 = mass2.value
        d = distance.value
        incl = inclination.value
        f = frequency.value
        p_zero = phi_zero.value

        tCoalNew = calcTcoal(m1, m2, f)

        # Generate the new curve
        x = tDomain(m1, m2, f)
        yPlus = hPlus(x, m1, m2, d, incl, f, p_zero)
        yCross = hCross(x, m1, m2, d, incl, f, p_zero)

        sourcePlus.data = dict(x=x-tCoalNew, y=yPlus)
        sourceCross.data = dict(x=x-tCoalNew, y=yCross)

        plot.x_range.start = -tCoalNew * 1.05
        plot.x_range.end = tCoalNew * .05
        plot.y_range.start = - hMax(m1, m2, d, incl, f, p_zero)
        plot.y_range.end =  hMax(m1, m2, d, incl, f, p_zero)


    for w in [mass1, mass2, distance, inclination, frequency, phi_zero]:
        w.on_change('value', update_data)


    # Set up layouts and add to document
    inputs = column(mass1, mass2, distance, inclination, frequency, phi_zero)

    # curdoc().add_root(row(inputs, plot, width=800))
    # curdoc().title = "GW Plot"
    doc.add_root(row(inputs, plot, width=800))
    doc.title = "GW Plot"


server = Server({'/': modify_doc}, num_procs=1)
server.start()

if __name__ == '__main__':
    print('Opening Bokeh application on http://localhost:5006/')

    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()

# html = file_html(plot, CDN, "my plot")
#
# Html_file= open("index.html","w")
# Html_file.write(html)
# Html_file.close()

# save(plot)
