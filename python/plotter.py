#!/bin/env python3

"""plotter

This module contains functions which are involved in plotting a map of the United States as well as the laboratories
and home institutions involved in the WDTS tracks programs.

Functions
---------
hanging_line
    Returns a numpy array representing a curved line between two (x,y) points
plot_map
    Does all of the formatting and plotting of the map, markers, and lines
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import pandas as pd

from laboratory import Laboratories
from person import Jobs
from utilities import get_formatted_filename

def hanging_line(point1, point2):
    """Load the correct database of postsecondary school locations

    From: https://stackoverflow.com/questions/30008322/draw-a-curve-connecting-two-points-instead-of-a-straight-line

    Parameters
    ----------
    point1 : list
        A list containing the x and y coordinates of a point in a Cartesian coordinate system
    point2 : list
        A list containing the x and y coordinates of a point in a Cartesian coordinate system

    Returns
    -------
    tuple
        A tuple of numpy arrays containing x and y coordinates that define a curved line between two points
    """

    #pylint: disable=C0103
    a = (point2[1] - point1[1])/(np.cosh(point2[0]) - np.cosh(point1[0]))
    b = point1[1] - a*np.cosh(point1[0])
    x = np.linspace(point1[0], point2[0], 100)
    y = a*np.cosh(x) + b

    return (x,y)

def plot_institution_markers(axes, legend_artists, lines, person_data, debug = False):
    """This function gets and plots the institution markers.

    Parameters
    ----------
    axes : list
        A list of axes.Axes on which to draw the markers
    legend_artists: list
        A list of matplotlib Line2D objects which will be used for the legend entries
    lines : bool
        Sets whether of not to draw the lines connecting the home institutions and the laboratories (yes = True, no = False)
    person_data : list
        The list of Person objects which contain the information to plot
    debug : bool, optional
        Print extra information useful for debugging issues
    """

    # get the university markers
    if lines:
        inst_df = pd.DataFrame(
            {
                'Inst': [person.home_institution.name for person in person_data if person.home_institution is not None],
                'Latitude': [person.home_institution.latitude for person in person_data if person.home_institution is not None],
                'Longitude': [person.home_institution.longitude for person in person_data if person.home_institution is not None],
            }
        )
        inst_gdf = gpd.GeoDataFrame(
            inst_df, geometry=gpd.points_from_xy(inst_df.Longitude, inst_df.Latitude)
        )
        if debug:
            print(inst_gdf.head())
        for axis in axes:
            inst_gdf.plot(ax = axis, color = 'blue')

        legend_artists.append(
            mlines.Line2D(
                [],
                [],
                color='blue',
                marker = ".",
                markersize=12,
                linestyle = None,
                linewidth = 0,
                label='Home Institution'
            )
        )
    else:
        # define a set of markers
        markers = ["o", "v", "^", "s", "p", "P", "D", "d", "X","*"]
        colors = [
            "lightskyblue", "deepskyblue", "cornflowerblue", "dodgerblue", "royalblue",
            "blue", "mediumblue", "darkblue", "navy", "midnightblue",
        ]

        # get the set of programs from list of people
        programs = set()
        for person in person_data:
            programs.add(person.program)

        if debug:
            print(programs)

        # loop over the programs and draw each on separately
        for iprogram, program in enumerate(sorted(programs)):
            inst_df = pd.DataFrame(
                {
                    'Inst': [person.home_institution.name for person in person_data \
                             if person.home_institution is not None and person.program == program],
                    'Latitude': [person.home_institution.latitude for person in person_data \
                                 if person.home_institution is not None and person.program == program],
                    'Longitude': [person.home_institution.longitude for person in person_data \
                                  if person.home_institution is not None and person.program == program],
                }
            )
            inst_gdf = gpd.GeoDataFrame(
                inst_df, geometry=gpd.points_from_xy(inst_df.Longitude, inst_df.Latitude)
            )
            if debug:
                print(inst_gdf.head())
            for axis in axes:
                inst_gdf.plot(ax = axis, color = colors[iprogram], marker = markers[iprogram])

            legend_artists.append(
                mlines.Line2D(
                    [],
                    [],
                    color = colors[iprogram],
                    marker = markers[iprogram],
                    markersize=12,
                    linestyle = None,
                    linewidth = 0,
                    label = f'Home Institution ({program})'
                )
            )

def plot_lab_markers(axes, legend_artists, debug = False):
    """This function gets and plots the laboratory markers.

    Parameters
    ----------
    axes : list
        A list of axes.Axes on which to draw the markers
    legend_artists: list
        A list of matplotlib Line2D objects which will be used for the legend entries
    debug : bool, optional
        Print extra information useful for debugging issues
    """

    lab_df = pd.DataFrame(
        {
            'Lab': [l.abbreviation for l in Laboratories.list_values()],
            'Latitude': [l.latitude for l in Laboratories.list_values()],
            'Longitude': [l.longitude for l in Laboratories.list_values()],
        }
    )
    lab_gdf = gpd.GeoDataFrame(
        lab_df, geometry=gpd.points_from_xy(lab_df.Longitude, lab_df.Latitude)
    )
    if debug:
        print(lab_gdf.head())
    for axis in axes:
        lab_gdf.plot(ax = axis, color = 'red', marker = '*', markersize = 60)

    legend_artists.insert(
        0,
        mlines.Line2D(
            [],
            [],
            color='red',
            marker = "*",
            markersize=12,
            linestyle = None,
            linewidth = 0,
            label='DOE Laboratory'
        )
    )

def plot_lines(axes, legend_artists, person_data):
    """This function plots the lines connecting institutions and labs

    Parameters
    ----------
    axes : list
        A list of axes.Axes on which to draw the markers
    legend_artists: list
        A list of matplotlib Line2D objects which will be used for the legend entries
    person_data : list
        The list of Person objects which contain the information to plot
    """

    legend_artists.append(mlines.Line2D([], [], color='orange', linestyle = "-", label='Faculty'))
    legend_artists.append(mlines.Line2D([], [], color='yellow', linestyle = "--", label='Student'))
    for person in person_data:
        if person.home_institution is None:
            continue
        start_location = [person.home_institution.longitude, person.home_institution.latitude]
        end_location = [person.host_doe_laboratory.value.longitude, person.host_doe_laboratory.value.latitude]
        x_coord, y_coord = hanging_line(start_location, end_location)
        for axis in axes:
            axis.plot(
                x_coord,
                y_coord,
                linewidth = 1 if person.job == Jobs.Student else 2,
                linestyle = "--" if person.job == Jobs.Student else "-",
                color = "yellow" if person.job == Jobs.Student else "orange"
            )

def plot_map(debug = False, formats = None, lines = True, output_path = "./", person_data = None, show = False, states = None):
    """This function does all of the formatting and plotting of the map, markers, and lines

    Matplotlib resources:
        * matplotlib colors - https://matplotlib.org/stable/gallery/color/named_colors.html
        * Tight left and right margins - https://stackoverflow.com/questions/4042192/reduce-left-and-right-margins-in-matplotlib-plot

    Other resources:
        * Data - https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html
        * Basic plotting - https://stackoverflow.com/questions/39742305/how-to-use-basemap-python-to-plot-us-with-50-states
        * Basic plotting - https://medium.com/@erikgreenj/mapping-us-states-with-geopandas-made-simple-d7b6e66fa20d
        * More advanced plotting - https://jcutrer.com/python/learn-geopandas-plotting-usmaps
        * Advanced plotting - https://geopandas.org/en/stable/gallery/plotting_basemap_background.html
        * Move AK and HI - https://stackoverflow.com/questions/69278742/rearranging-polygons-in-geopandas-for-matplotlib-plotting

    Parameters
    ----------
    debug : bool, optional
        Print extra information useful for debugging issues
    formats : list, optional
        A list of strings of the desired output formats for the map
    lines : bool, optional
        Sets whether of not to draw the lines connecting the home institutions and the laboratories (yes = True, no = False)
    output_path : str, optional
        The path to the directory in which to save the output file
    person_data : list, optional
        The list of Person objects which contain the information to plot
    show : bool, optional
        If True, an interactive version of the output plot is printed to the screen
    states : list, optional
        A list of state abbreviations which determines a subset of states to plot
    """

    # create an axis with the insets − this defines the inset sizes
    fig, continental_ax = plt.subplots(figsize=(20, 10))
    alaska_ax = continental_ax.inset_axes([.055, -.0525, .225, .315]) # [x0, y0, width, height]
    hawaii_ax = continental_ax.inset_axes([.279, .01, .15, .19]) # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.inset_axes.html
    puerto_rico_ax = continental_ax.inset_axes([.8, -.01, .15, .19])
    set_axes_bounds(continental_ax, alaska_ax, hawaii_ax, puerto_rico_ax)

    # plot the US map
    plot_us_map(continental_ax, alaska_ax, hawaii_ax, puerto_rico_ax, debug = debug, states = states)

    # start keeping track of the legend items
    legend_artists = []

    # plot the institution markers and add the markers to the legend
    plot_institution_markers([continental_ax, alaska_ax, hawaii_ax, puerto_rico_ax], legend_artists, lines, person_data, debug = debug)

    # plot the laboratory markers
    plot_lab_markers([continental_ax, alaska_ax, hawaii_ax, puerto_rico_ax], legend_artists, debug = debug)

    # draw the lines between labs and institutions
    if lines:
        plot_lines([continental_ax, alaska_ax, hawaii_ax, puerto_rico_ax], legend_artists, person_data)

    # add a legend
    continental_ax.legend(handles=legend_artists, prop={'size': 16}, facecolor='Grey', loc='upper right')

    # remove ticks
    remove_axis_ticks([continental_ax, alaska_ax, hawaii_ax, puerto_rico_ax])

    # remove the axes altogether
    #plt.axis('off')

    # reduce the left and right margins
    fig.tight_layout()

    # save the figure
    if formats is not None:
        save_figure(formats, output_path)

    if show:
        plt.show()

def plot_us_map(continental_ax, alaska_ax, hawaii_ax, puerto_rico_ax, debug = False, states = None):
    """This function plots the map of the United States on the predefined axes.

    Parameters
    ----------
    continental_ax : axes.Axes
        The axes containing the continental US map
    alaska_ax : axes.Axes
        The inset axes containing the the map of Alaska
    hawaii_ax : axes.Axes
        The inset axes containing the the map of Hawaii
    puerto_rico_ax : axes.Axes
        The inset axes containing the the map of Puerto Rico
    debug : bool, optional
        Print extra information useful for debugging issues
    states : list, optional
        A list of state abbreviations which determines a subset of states to plot
    """

    # open the GeoDataFrame for the map of the United States
    usa = gpd.read_file("data/us_map/cb_2020_us_state_500k.shp")

    # set state code as index, exclude states that we will never display
    usa = usa.set_index('STUSPS').drop(index=['VI', 'MP', 'GU', 'AS'])
    if debug:
        print(usa[['NAME','geometry']])

    # Plot the data per area - requires passing the same choropleth parameters to each call
    # because different data is used in each call, so automatically setting bounds won’t work
    usa.drop(index=['HI', 'AK', 'PR']).plot(ax = continental_ax, color = "Grey", linewidth = 0.25, edgecolor = 'k')
    usa.loc[['AK']].plot(ax = alaska_ax, color = "Grey", linewidth = 0.25, edgecolor = 'k')
    usa.loc[['HI']].plot(ax = hawaii_ax, color = "Grey", linewidth = 0.25, edgecolor = 'k')
    usa.loc[['PR']].plot(ax = puerto_rico_ax, color = "Grey", linewidth = 0.25, edgecolor = 'k')

    if states is not None:
        selection = usa[usa.index.isin(states)]
        selection.plot(ax = continental_ax, cmap = 'OrRd', figsize = (25, 14)) # color = "DarkGray"

def remove_axis_ticks(axes):
    """This function removes the tick marks from a set of axes

    Parameters
    ----------
    axes : list
        A list of axes.Axes
    """

    for axis in axes:
        axis.set_yticks([])
        axis.set_xticks([])

def save_figure(formats, output_path):
    """Save the current plot to a file

    Parameters
    ----------
    formats : list, optional
        A list of strings of the desired output formats for the map
    output_path : str, optional
        The path to the directory in which to save the output file
    """

    for fmt in formats:
        output_filename = get_formatted_filename(f"{output_path}", "map", fmt)
        plt.savefig(output_filename, bbox_inches='tight')

def set_axes_bounds(continental_ax, alaska_ax, hawaii_ax, puerto_rico_ax):
    """Set the bounds to fit desired areas in each plot.

    Parameters
    ----------
    continental_ax : axes.Axes
        The axes containing the continental US map
    alaska_ax : axes.Axes
        The inset axes containing the the map of Alaska
    hawaii_ax : axes.Axes
        The inset axes containing the the map of Hawaii
    puerto_rico_ax : axes.Axes
        The inset axes containing the the map of Puerto Rico
    """

    continental_ax.set_xlim(-130, -64)
    continental_ax.set_ylim(22, 53)

    alaska_ax.set_ylim(51, 72)
    alaska_ax.set_xlim(-180, -127)

    hawaii_ax.set_ylim(18.8, 22.5)
    hawaii_ax.set_xlim(-160, -154.6)

    puerto_rico_ax.set_ylim(17.5, 19)
    puerto_rico_ax.set_xlim(-68.25, -65)
