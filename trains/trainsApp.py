# -*- coding: UTF-8 -*-
'''
Kiwiland Trains App by Patrick Gitundu
'''


# Import required libraries
from __future__ import print_function
from flask import Flask,render_template,request,jsonify,url_for
import networkx as nx
import json
from trains import app



# Establish the home page routes
@app.route("/")
@app.route("/kiwiland_trains")
def main():
    return render_template('index.html')                # Render the page

     
G = nx.DiGraph()                                        # Create graph
nodes = ['A','B','C','D','E']                           # Create nodes. 
w_edges = [('A','B',5), ('B','C',4), ('C','D',8), ('D','C',8), ('D','E',6), ('A','D',5), ('C','E',2), ('E','B',3), ('A','E',7)] # Create weighted edges
G.add_nodes_from(nodes)                                                                                                         # Add selected nodes to graph
G.add_weighted_edges_from(w_edges)                                                                                              # Add edges to the graph

'''
@pre: gets passed three variables. The first two should be a capitalized alphabetic character. The third should be a number
@post: 
@returns: array 
'''
def numberOfTrips(source,dest,cutoff):
    matched_paths = []                                  # Collection of paths that meet the requirements set by the user
    paths = nx.all_simple_paths(G,source,dest,cutoff)   # Retrieve all paths possible using the source and destination
    for path in paths:                                  
        if len(path) == (cutoff+1):                     # If number of nodes in the path is the same as the cutoff target, add the path to the required paths
            matched_paths.append(path)
        if len(path) < (cutoff+1):
            if sum(1 for rp in nx.all_simple_paths(G,dest,dest,cutoff= ((cutoff+1)-len(path)))) != 0:   #
                rem_path = nx.all_simple_paths(G,dest,dest,cutoff= ((cutoff+1)-len(path)))
                for rp in rem_path:
                    for c in range(((cutoff+1)-len(path)),0,-1):
                        path.append(rp[-c])
            if len(path) == (cutoff+1):
                matched_paths.append(path)
    return matched_paths

'''
@pre: receives source and destination stations.
@post: processes all paths possible between the orgin and destination
@returns: array
'''
def shortestRoutes(source,dest):
    path_lengths = []                                   #collection of path lengths of all paths possible between the origin and destination
    path = nx.all_simple_paths(G,source,dest)           #retrieve all paths possible using the source and destination
    for p in path:
        length = 0;
        for i in range(len(p)):
            try:
                length += nx.dijkstra_path_length(G, p[i], p[i+1])  #add the length of each path to the overall path length
            except IndexError as e:
                break;
        path_lengths.append(length)                     #add the length of each path to the collection of paths
    return path_lengths                                 #opted to return an array instead of the smallest value to provide for loops/cycles that are not possible 

'''
@pre: gets passed an array of stations for a path.
@post: iterates over the path adding the length of each connection to the length of the path
@returns: integer
'''
def getLength(p):
    length = 0                                          #Initialize the length of the path to zero
    for i in range(len(p)):
        try:
            length += nx.dijkstra_path_length(G, p[i], p[i+1])  #add the length of each connection in the path to the overall path length
        except IndexError as e:
            break;
    return length                                       #return the length of the path

'''
@pre: gets passed the source, destination and distance to be covered
@post: finds all paths with a total distance length less than the distance set by the user
@returns: array
'''
def addToPaths(mp,dest,distance):
    mpl_temp =[]
    for mpl in mp:                                       # Create a collection of temporary paths
        mpl_sub = list(mpl)                                         # If any paths were missed this collection of loops will identify them and add them to the larger collection
        for ps in nx.all_simple_paths(G,dest,dest):                 # This was necessitated because some expected routes were not being retrieved as expected
            if (getLength(mpl_sub) + getLength(ps)) < distance:
                ps_sub = ps[1:len(ps)]
                new_mp = list(mpl_sub) + list(ps_sub)
                if new_mp not in mp:
                    mpl_temp.append(new_mp)
    return mpl_temp

def numberOfDifferentTrips(source,dest,distance):
    matched_paths = []
    paths = nx.all_simple_paths(G,source,dest,distance)
    try:    
        for p in paths:
            length = getLength(p)
            if length < (distance):
                matched_paths.append(p)                 #add any paths that have a length less than the target distance to the collection of paths
        
        while len(addToPaths(matched_paths,dest,distance)) > 0:
            new_paths = addToPaths(matched_paths,dest,distance)
            for p in new_paths:
                matched_paths.append(p)
        
    except Exception as e:
        print(str(e))
    
    return matched_paths 

metric = stops = distance = maxexact = ''
stations = []

def getOutput(metric,stations,stops,distance,maxexact):
    try:                                                                                    # Retrieve variables set by the user
        output = 0
        try:
           if (len(stations) == 2):                                                        # Most scenarios will involve two stations so they will be addressed first; Loops(such as C-C) are counted as two stations 
               if (metric == '1'):                                                         # User selects 'Calculate Route Distance'
                   if (G.has_edge(stations[0],stations[1])):                               # As per the instructions for the output, if a direct link exists between the source and destination
                       output += nx.dijkstra_path_length(G, stations[0], stations[1])      # respond with the length of the path
                   else:
                       output = 'This route does not exist'                                # If no connection exists, respond that the route selected does not exist
                
               elif (metric == '2' and stops < 0):                                         # User selects 'Number of Trips' but no indicated stops
                   paths = nx.all_simple_paths(G,stations[0], stations[1])                 # Find all paths between station 1 and station 2
                   num_paths = sum(1 for p in paths)                                       # Find the number of paths
                   if (num_paths <= 0):                                                    # If the number of paths is less than or equal to 0, respond that the rout configuration is not possible
                       output = 'This route configuration is not possible.'
                   else:                                                                   # If the number of paths is greater than 0 respond with the number of paths for that combination of stations selected 
                        output = num_paths,' Trips are possible.'
                
               elif (metric == '2' and stops > 0 and maxexact == '1'):                     # User selects 'Number of Trips', indicates approximate maximum number of stops required
                   paths = nx.all_simple_paths(G,stations[0],stations[1],cutoff=stops)     # Retrieve all paths shorter than or equal to the specified number of stops
                   nt = sum(1 for p in paths)                                              # Find the number of paths
                   if (nt <= 0):
                       output = 'This route configuration is not possible.'                 # Respond with the number of trips 
                   else:
                       output = nt,' Trips are possible.'
                
               elif (metric == '2' and stops > 0 and maxexact == '2'):                     # User selects 'Number of Trips', indicates exact number of stops required
                   nt = numberOfTrips(stations[0], stations[1], stops)                     # Retrieve all paths equal to the specified number of stops
                   if (len(nt) <= 0):
                       output = 'This route configuration is not possible'                 # Respond with the number of trips that match the number of stops exactly
                   else:
                       output = len(nt),' Trips are possible.'
                
               elif (metric == '3'):                                                       # User selects 'Shortest Route Length', indicates exact number of stops required
                   path_lengths = shortestRoutes(stations[0], stations[1])
                   if(len(path_lengths) > 0):
                       output = min(path_lengths),' is the shortest route distance possible.'
                   else:
                       output = 'This route configuration is not possible.'
                
               elif (metric == '4' and maxexact == '1' and distance > 0):                          # User selects 'Number of Routes to Destination', indicates approximate maximum distance to be covered
                   paths = numberOfDifferentTrips(stations[0], stations[1], distance)               # Retrieve all paths shorter than or equal to the distance specified
                   if (len(paths) != 0):
                       output = len(paths),' possible routes.'                                      # Respond with number of routes possible
                   else:
                       output = 'This route configuration is not possible.'
            
           elif (len(stations) > 2):                                                               # Scenarios involving  more than two stations
               if (metric == '1'):                                                                 # User selects 'Calculate Route Distance'
                   for i,station in enumerate(stations):                       
                       try:
                           if (G.has_edge(stations[i],stations[i+1])):                             # As per the instructions for the output, if a direct link exists between the source and destination
                               output += nx.dijkstra_path_length(G, stations[i], stations[i+1])    # Respond with the length of the path
                           else:
                               output = 'This route does not exist.'                                # If no connection exists, respond that the route selected does not exist
                       except IndexError as e:
                           break;
               elif (metric == '2' or metric == '3' or metric == '4'):
                   output = 'This route configuration is not possible.'
        except Exception as e:
            print (str(e))
         
        return jsonify(result = output)

    except Exception as e:
        print (str(e))

    
@app.route('/getOutput')
def getData():
    try:
        metric = request.args.get('metric')
        stations = request.args.getlist('stations[]')
        stops = request.args.get('stops',type=int)
        if stops is None :
            stops = -1        
        distance = request.args.get('distance',type=int)
        if distance is None:
            distance = -1
        maxexact = request.args.get('maxexact',type=str)
        
        result = getOutput(metric, stations, stops, distance, maxexact)
        return result
    except Exception as e:
        print(str(e))
  
