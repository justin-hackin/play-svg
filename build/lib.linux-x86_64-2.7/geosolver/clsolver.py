"""A generic geometric constraint solver. 

This module provides basic functionality for 
ClusterSolver2D and ClusterSolver3D.

The solver finds a generic solution
for problems formulated by Clusters. The generic solution 
is a directed acyclic graph of Clusters and Methods. Particilar problems
and solutions are represented by a Configuration for each cluster.
"""

from graph import Graph
from method import Method, MethodGraph
from diagnostic import diag_print
from notify import Notifier
from sets import Set, ImmutableSet
from multimethod import MultiVariable, MultiMethod
from cluster import *
from configuration import Configuration

# Basic methods 

class ClusterMethod(MultiMethod):
    """A derive is a method such that a single ouput cluster is a 
    subconsraint of a single input cluster."""

    def __init__(self):
        self.consistent = None
        self.overconstrained = None
        MultiMethod.__init__(self)

    def prototype_constraints(self):
        return []

    def status_str(self):
        s = ""
        if self.consistent == True:
            s += "consistent "
        elif self.consistent == False:    
            s += "inconsistent "
        if self.overconstrained == True:
            s += "overconstrained"
        elif self.overconstrained == False:
            s += "wellconstrained"
        return s


class PrototypeMethod(MultiMethod):
    """A PrototypeMethod selects those solutions of a cluster for which
       the protoype and the solution satisfy the same constraints.
    """

    def __init__(self, incluster, selclusters, outcluster, constraints):
        self._inputs = [incluster]+selclusters
        self._outputs = [outcluster]
        self._constraints = constraints
        MultiMethod.__init__(self)

    def multi_execute(self, inmap):
        diag_print("PrototypeMethod.multi_execute called","clmethods")
        incluster = self._inputs[0] 
        selclusters = []
        for i in range(1,len(self._inputs)):
            selclusters.append(self._inputs[i])
        diag_print("input clusters"+str(incluster), "PrototypeMethod.multi_execute")
        diag_print("selection clusters"+str(selclusters), "PrototypeMethod.multi_execute")
        # get confs
        inconf = inmap[incluster]
        selmap = {}
        for cluster in selclusters:
            conf = inmap[cluster]
            assert len(conf.vars()) == 1
            var = conf.vars()[0]
            selmap[var] = conf.map[var]
        selconf = Configuration(selmap)
        sat = True
        diag_print("input configuration = "+str(inconf), "PrototypeMethod.multi_execute")
        diag_print("selection configuration = "+str(selconf), "PrototypeMethod.multi_execute")
        for con in self._constraints:
            satcon = con.satisfied(inconf.map) != con.satisfied(selconf.map)
            diag_print("constraint = "+str(con), "PrototypeMethod.multi_execute")
            diag_print("constraint satisfied? "+str(satcon), "PrototypeMethod.multi_execute")
            sat = sat and satcon
        diag_print("prototype satisfied? "+str(sat), "PrototypeMethod.multi_execute")
        if sat:
            return [inconf]
        else:
            return []
            
def is_information_increasing(method):
        infinc = True
        connected = Set()
        output = method.outputs()[0]
        for cluster in method.inputs():
            if num_constraints(cluster.intersection(output)) >= num_constraints(output):
		infinc = False
                break
        return infinc

# ---------- main class --------------

class ClusterSolver(Notifier):
    """Constraints are Clusers: Rigids, Hedgehogs and Balloons. 
       After adding each cluster, the solver tries to merge
       clusters, adding new clusters and methods between clusters. 
    """
    # ------- PUBLIC METHODS --------

    def __init__(self, dimension):
        """Create a new empty solver"""
        Notifier.__init__(self)
        self.dimension = dimension
        self._graph = Graph()
        self._graph.add_vertex("_root")
        self._graph.add_vertex("_toplevel")
        self._graph.add_vertex("_variables")
        self._graph.add_vertex("_distances")
        self._graph.add_vertex("_angles")
        self._graph.add_vertex("_rigids")
        self._graph.add_vertex("_hedgehogs")
        self._graph.add_vertex("_balloons")
        self._graph.add_vertex("_methods")
        # queue of new objects to process
        self._new = []
        # methodgraph 
        self._mg = MethodGraph()
         
    def variables(self):
        """get list of variables"""
        return self._graph.outgoing_vertices("_variables")

    def distances(self):
        """get list of distances"""
        return self._graph.outgoing_vertices("_distances")

    def angles(self):
        """get list of angles"""
        return self._graph.outgoing_vertices("_angles")

    def rigids(self):
        """get list of rigids"""
        return self._graph.outgoing_vertices("_rigids")

    def hedgehogs(self):
        """get list of hedgehogs"""
        return self._graph.outgoing_vertices("_hedgehogs")

    def balloons(self):
        """get list of balloons"""
        return self._graph.outgoing_vertices("_balloons")

    def methods(self):
        """get list of methods"""
        return self._graph.outgoing_vertices("_methods")

    def top_level(self):
        """get top-level objects"""
        return self._graph.outgoing_vertices("_toplevel")

    def is_top_level(self, object):
        return self._graph.has_edge("_toplevel",object)

    def add(self, cluster):
        """Add a cluster. 
        
           arguments:
              cluster: A Rigid
           """
        diag_print("add_cluster "+str(cluster), "clsolver")
        self._add_cluster(cluster)
        self._process_new()

    def remove(self, cluster):
        """Remove a cluster. 
           All dependend objects are also removed.
        """
        self._remove(cluster)
        self._process_new()

    def set(self, cluster, configurations):
        """Associate a list of configurations with a cluster"""
        self._mg.set(cluster, configurations)
        
    def get(self, cluster):
        """Return a set of configurations associated with a cluster"""
        return self._mg.get(cluster)
 
    def set_root(self, rigid):
        """Make given rigid cluster the root cluster
        
           arguments:
              cluster: A Rigid
           """
        self._graph.rem_vertex("_root")
        self._graph.add_edge("_root", rigid)
       
    def find_dependend(self, object):
        """Return a list of objects that depend on given object directly."""
        l = self._graph.outgoing_vertices(object)
        return filter(lambda x: self._graph.get(object,x) == "dependency", l)
        
    def find_depends(self, object):
        """Return a list of objects that the given object depends on directly"""
        l = self._graph.ingoing_vertices(object)
        return filter(lambda x: self._graph.get(x,object) == "dependency", l)

    def contains(self, obj):
        return self._graph.has_vertex(obj)

    # ------------ INTERNALLY USED METHODS --------

    # -- general house hold

    def _add_dependency(self, on, dependend):
        """Add a dependence for second object on first object"""
        self._graph.add_edge(on, dependend, "dependency")

    def _add_to_group(self, group, object):
        """Add object to group"""
        self._graph.add_edge(group, object, "contains")

    def _add_needed_by(self, needed, by):
        """Add relation 'needed' object is needed 'by'"""
        self._graph.add_edge(needed, by, "needed_by")

    def _objects_that_need(self, needed):
        """Return objects needed by given object"""
        l = self._graph.outgoing_vertices(needed)
        return filter(lambda x: self._graph.get(needed,x) == "needed_by", l)

    def _objects_needed_by(self, needer):
        """Return objects needed by given object"""
        l = self._graph.ingoing_vertices(needer)
        return filter(lambda x: self._graph.get(x,needer) == "needed_by", l)
   
    def _add_top_level(self, object):
        self._graph.add_edge("_toplevel",object)
        self._new.append(object)

    def _rem_top_level(self, object):
        self._graph.rem_edge("_toplevel",object)
        if object in self._new:
            self._new.remove(object)

    def _remove(self, object):
        # find all indirectly dependend objects
        todelete = [object]+self._find_descendend(object)
        torestore = Set()
        # remove all objects
        for item in todelete:
            # if merge removed items from toplevel then add them back to top level 
            if hasattr(item, "restore_toplevel"):
                for cluster in item.restore_toplevel:
                    torestore.add(cluster)
            # delete it from graph
            diag_print("deleting "+str(item),"clsolver.remove")
            self._graph.rem_vertex(item)
            # remove from _new list
            if item in self._new:
                self._new.remove(item)
            # remove from methodgraph
            if isinstance(item, Method):
                # note: method may have been removed because variable removed
                try:
                    self._mg.rem_method(item)
                except:
                    pass
            elif isinstance(item, MultiVariable):
                self._mg.rem_variable(item)
            # notify listeners
            self.send_notify(("remove", item))
        # restore toplevel (also added to _new)
        for cluster in torestore:
            if self._graph.has_vertex(cluster): 
                self._add_top_level(cluster)
        # debug
        # print "after remove, drplan:"
        # print self
        # print "after remove, toplevel:"
        # print self.top_level()
        # re-solve
        self._process_new()

    def _find_descendend(self,v):
        """find all descendend objects of v (dirdctly or indirectly dependend"""
        front = [v]
        result = {}
        while len(front) > 0:
            x = front.pop()
            if x not in result:
                result[x] = 1
                front += self.find_dependend(x)
        del result[v]
        return list(result)


    # -- add object types
   
    def _add_variable(self, var):
        """Add a variable if not already in system
        
           arguments:
              var: any hashable object
        """
        if not self._graph.has_vertex(var):
            diag_print("_add_variable "+str(var), "clsolver")
            self._add_to_group("_variables", var)

    def _add_cluster(self, cluster):
        if isinstance(cluster, Rigid):
            self._add_rigid(cluster)
        elif isinstance(cluster, Hedgehog):
            self._add_hog(cluster)
        elif isinstance(cluster, Balloon):
            self._add_balloon(cluster)
        else:
            raise StandardError, "unsupported type", type(cluster)

    def _add_rigid(self, newcluster):
        """add a rigid cluster if not already in system"""
        diag_print("_add_rigid "+str(newcluster),"clsolver")
        # check if not already exists
        if self._graph.has_vertex(newcluster): 
            raise StandardError, "rigid already in clsolver"
        # update graph
        self._add_to_group("_rigids", newcluster)
        for var in newcluster.vars:
            self._add_variable(var)
            self._add_dependency(var, newcluster)
        # if there is no root cluster, this one will be it
        if len(self._graph.outgoing_vertices("_root")) == 0:
            self._graph.add_edge("_root", newcluster)
        # add to top level
        self._add_top_level(newcluster)
        # add to methodgraph
        self._mg.add_variable(newcluster)
        # notify
        self.send_notify(("add", newcluster))
    #end def _add_rigid

    def _add_hog(self, hog):
        diag_print("_add_hog:"+str(hog), "clsolver")
        # check if not already exists
        if self._graph.has_vertex(hog): 
            raise StandardError, "hedgehog already in clsolver"
        # update graph
        self._add_to_group("_hedgehogs",hog)
        for var in list(hog.xvars)+[hog.cvar]:
            self._add_variable(var)
            self._add_dependency(var, hog)
        # add to top level
        self._add_top_level(hog)
        # add to methodgraph
        self._mg.add_variable(hog)
        # notify 
        self.send_notify(("add", hog))

    def _add_balloon(self, newballoon):
        """add a cluster if not already in system"""
        diag_print("_add_balloon "+str(newballoon),"clsolver")
        # check if not already exists
        if self._graph.has_vertex(newballoon): 
            raise StandardError, "balloon already in clsolver"
        # update graph
        self._add_to_group("_balloons", newballoon)
        for var in newballoon.vars:
            self._add_variable(var)
            self._add_dependency(var, newballoon)
        # add to top level
        self._add_top_level(newballoon)
         # add to methodgraph
        self._mg.add_variable(newballoon)
        # notify 
        self.send_notify(("add", newballoon))
    #end def _add_balloon

    def _add_merge(self, merge):
        # structural check that method has one output
        if len(merge.outputs()) != 1:
            raise StandardError, "merge number of outputs != 1"
        output = merge.outputs()[0]
        # remove any derives from clusters to be merged
        #for cluster in merge.inputs():
        #    outgoing = self.find_dependend(cluster)
        #    derives = filter(lambda x: isinstance(x, Derive), outgoing)
        #    for d in derives:
        #        self._remove(d)
        # consistent merge?
        consistent = True
        for i1 in range(0, len(merge.inputs())):
            for i2 in range(i1+1, len(merge.inputs())):
                c1 = merge.inputs()[i1] 
                c2 = merge.inputs()[i2] 
                consistent = consistent and self._is_consistent_pair(c1, c2)
        merge.consistent = consistent
        # overconstrained cluster?
        overconstrained = not consistent
        for cluster in merge.inputs():
            overconstrained = overconstrained and cluster.overconstrained
        output.overconstrained = overconstrained
        # add to graph
        self._add_cluster(output)
        self._add_method(merge)
        # remove inputs from toplevel
        for cluster in merge.inputs():
            self._rem_top_level(cluster)  
        # add prototype selection method
        self._add_prototype_selector(merge)
        # add solution selection method
        self._add_solution_selector(merge)

    def _add_prototype_selector(self, merge):
        incluster = merge.outputs()[0]
        constraints = merge.prototype_constraints()
        if len(constraints) == 0: 
            return
        vars = Set()
        for con in constraints:
            vars.union_update(con.variables())
        selclusters = []
        for var in vars:
            clusters = self._graph.outgoing_vertices(var)
            clusters = filter(lambda c: isinstance(c, Rigid), clusters)
            clusters = filter(lambda c: len(c.vars) == 1, clusters)
            if len(clusters) != 1:
                raise StandardError, "no prototype cluster for variable "+str(v)
            selclusters.append(clusters[0])
        outcluster = incluster.copy()
        # Rick 20090519 - copy does not copy structural overconstrained flag?
        outcluster.overconstrained = incluster.overconstrained
	selector = PrototypeMethod(incluster, selclusters, outcluster, constraints)
        self._add_cluster(outcluster)
        self._add_method(selector)
        self._rem_top_level(incluster)
        return

    def _add_solution_selector(self, merge):
        return

    def _add_method(self, method):
        diag_print("new "+str(method),"clsolver")
        self._add_to_group("_methods", method)
        for obj in method.inputs():
            self._add_dependency(obj, method)
        for obj in method.outputs():
            self._add_dependency(method, obj)
            self._add_dependency(obj, method)
        self._mg.add_method(method)
        self.send_notify(("add", method))
 
        
    # --------------
    # search methods
    # --------------
 
    def _process_new(self):
        while len(self._new) > 0:
            newobject = self._new.pop()
            diag_print ("search from "+str(newobject), "clsolver")
            succes = self._search(newobject)
            if succes and self.is_top_level(newobject): 
                # maybe more rules applicable.... push back on stack
                self._new.append(newobject)
        # while
    #end def

    def _search(self, newcluster):
        raise StandardError, "Not implemented. ClusterSolver is an abstract class, please use ClusterSolver2D or ClusterSolver3D"

    def _contains_root(self, input_cluster):
        """returns True iff input_cluster is root cluster or was determined by
        merging with the root cluster."""

        # start from root cluster. Follow merges upwards until:
        #  - input cluster found -> True
        #  - no more merges -> False
    
        if len(self._graph.outgoing_vertices("_root")) > 1:
            raise StandardError, "more than one root cluster" 
        if len(self._graph.outgoing_vertices("_root")) == 1:
            cluster = self._graph.outgoing_vertices("_root")[0]
        else:
            cluster = None
        while (cluster != None):
            if cluster is input_cluster:
                return True
            fr = self._graph.outgoing_vertices(cluster)
            me = filter(lambda x: isinstance(x, Merge), fr)
            me = filter(lambda x: cluster in x.outputs(), me)
            if len(me) > 1:
                raise StandardError, "root cluster merged more than once"
            elif len(me) == 0:
                cluster = None
            elif len(me[0].outputs()) != 1:
                raise StandardError, "a merge with number of outputs != 1"
            else:
                cluster = me[0].outputs()[0]
        #while
        return False
    #def

    def _is_consistent_pair(self, object1, object2):
        diag_print("in is_consistent_pair "+str(object1)+" "+str(object2),"clsolver")
        oc = over_constraints(object1, object2) 
        diag_print("over_constraints: "+str(map(str,oc)),"clsolver")
        consistent = True
        for con in oc:
            consistent = consistent and self._consistent_overconstraint_in_pair(con, object1, object2)
        diag_print("global consistent? "+str(consistent),"clsolver")
        return consistent
    
    def _consistent_overconstraint_in_pair(self, overconstraint, object1, object2):
        diag_print("consistent "+str(overconstraint)+" in "+str(object1)+" and "+str(object2)+" ?", "clsolver")
    
        # get sources for constraint in given clusters
        s1 = self._source_constraint_in_cluster(overconstraint, object1)
        s2 = self._source_constraint_in_cluster(overconstraint, object2)

        if s1 == None:
            consistent = False
        elif s2 == None:
            consistent = False
        elif s1 == s2:
            consistent = True
        else:
            if self._is_atomic(s1) and not self._is_atomic(s2):
                consistent = False
            elif self._is_atomic(s2) and not self._is_atomic(s1):
                consistent = False
            else:
                consistent = True
            #c1to2 = constraits_from_s1_in_s2(s1, s2)
            #if solve(c1to2) contains overconstraint then consistent
            #c2to1 = constraits_from_s1_in_s2(s2, s1)
            #if solve(c2to1) contains overconstraint then consistent
            #raise StandardError, "not yet implemented"

        diag_print("consistent? "+str(consistent), "clsolver")
        return consistent

    def _source_constraint_in_cluster(self, constraint, cluster):
        if not self._contains_constraint(cluster, constraint):
            raise StandardError, "constraint not in cluster"
        elif self._is_atomic(cluster):
            return cluster
        else:
            method = self._determining_method(cluster)
            inputs = method.inputs()
            down = filter(lambda x: self._contains_constraint(x, constraint), inputs)
            if len(down) == 0:
                return cluster
            elif len(down) > 1:
                if method.consistent == True:
                    return self._source_constraint_in_cluster(constraint, down[0])
                else: 
                    diag_print("Warning: source is inconsistent","clsolver")
                    return None
            else:
                return self._source_constraint_in_cluster(constraint, down[0])

           
    def _is_atomic(self, object):
        method = self._determining_method(object)
        if method == None:
            return True
        #elif isinstance(method, Distance2Rigid) or isinstance(method, Angle2Hog):
        #    return True
        else:
            return False

    def _determining_method(self, object):
        depends = self.find_depends(object)
        methods = filter(lambda x: isinstance(x, Method), depends)
        if len(methods) == 0:
            return None
        elif len(methods) > 1:
            raise "object determined by more than one method"
        else:
            return methods[0] 

    
    def _contains_constraint(self, object, constraint):
        if isinstance(constraint, Distance):
            return self._contains_distance(object, constraint)
        elif isinstance(constraint, Angle):
            return self._contains_angle(object, constraint)
        else:
            raise StandardError, "unexpected case"

    def _contains_distance(self,object, distance):
        if isinstance(object, Rigid):
            return (distance.vars[0] in object.vars and distance.vars[1] in object.vars)
        elif isinstance(object, Distance):
            return (distance.vars[0] in object.vars and distance.vars[1] in object.vars)
        else:
            return False

    def _contains_angle(self, object, angle):
        if isinstance(object, Rigid) or isinstance(object, Balloon):
            return (angle.vars[0] in object.vars 
            and angle.vars[1] in object.vars 
            and angle.vars[2] in object.vars)
        elif isinstance(object, Hedgehog):
            return (angle.vars[1] == object.cvar and
            angle.vars[0] in object.xvars and 
            angle.vars[2] in object.xvars)
        elif isinstance(object, Angle):
            return (angle.vars[1] == object.vars[1] and
            angle.vars[0] in object.vars and 
            angle.vars[2] in object.vars)
        else:
            return False


    # --------- special methods ------

    def __str__(self):
        s = ""
        for x in self.distances():
            s += str(x) + "\n"
        for x in self.angles():
            s += str(x) + "\n"
        for x in self.rigids():
            s += str(x) + "\n"
        for x in self.hedgehogs():
            s += str(x) + "\n"
        for x in self.balloons():
            s += str(x) + "\n"
        for x in self.methods():
            s += str(x) + "\n"
        return s

    # ---------- older unused methods, kept for possible future use ---------

    ##def _known_distance(self,a,b):
    ##    """returns Distance or Rigid that contains a and b"""
    ##    # get objects dependend on a and b
    ##    dep_a = self._graph.outgoing_vertices(a)
    ##    dep_b = self._graph.outgoing_vertices(b)
    ##    dependend = []
    ##    for obj in dep_a:
    ##        if obj in dep_b:
    ##            dependend.append(obj)
    ##    # find a Distance
    ##    # distances = filter(lambda x: isinstance(x,Distance), dependend)
    ##    # if len(distances) > 0: return distances[0]
    ##    # or find a Rigid
    ##    clusters = filter(lambda x: isinstance(x,Rigid), dependend)
    ##    clusters = filter(lambda x: self.is_top_level(x), clusters)
    ##    if len(clusters) > 0: return clusters[0]
    ##    # or return None
    ##    return None
    ##
   
    def _known_angle(self,a,b,c):
        """returns Balloon, Rigid or Hedgehog that contains angle(a, b, c)"""
        if a==b or a==c or b==c:
            raise StandardError, "all vars in angle must be different"
        # get objects dependend on a, b and c
        dep_a = self._graph.outgoing_vertices(a)
        dep_b = self._graph.outgoing_vertices(b)
        dep_c = self._graph.outgoing_vertices(c)
        dependend = []
        for obj in dep_a:
            if obj in dep_b and obj in dep_c:
                dependend.append(obj)
        # find a hedgehog
        hogs = filter(lambda x: isinstance(x,Hedgehog), dependend)
        hogs = filter(lambda hog: hog.cvar == b, hogs)
        hogs = filter(lambda x: self.is_top_level(x), hogs)
        if len(hogs) == 1: return hogs[0]
        if len(hogs) > 1: raise "error: angle in more than one hedgehogs"
        # or find a cluster
        clusters = filter(lambda x: isinstance(x,Rigid), dependend)
        clusters = filter(lambda x: self.is_top_level(x), clusters)
        if len(clusters) == 1: return clusters[0]
        if len(clusters) > 1: raise "error: angle in more than one Rigids"
        # or find a balloon
        balloons = filter(lambda x: isinstance(x,Balloon), dependend)
        balloons = filter(lambda x: self.is_top_level(x), balloons)
        if len(balloons) == 1: return balloons[0]
        if len(balloons) > 1: raise "error: angle in more than one Balloons"
        # or return None
        return None
    
    ##def _is_source(self, object, constraint):
    ##    if not self._contains_constraint(object, constraint):
    ##        return False
    ##    elif self._is_atomic(object):
    ##        return True
    ##    else:
    ##        method = self._determining_method(object)
    ##        inputs = method.inputs()
    ##        for object in inputs:
    ##            if self._contains_constraint(object, constraint):
    ##                return False
    ##        return True

    ##def _distance_sources(self, distance):
    ##    # find coincident clusters
    ##    dep_a = self._graph.outgoing_vertices(distance.vars[0])
    ##    dep_b = self._graph.outgoing_vertices(distance.vars[1])
    ##    dependend = []
    ##    for obj in dep_a:
    ##        if obj in dep_b:
    ##            dependend.append(obj)
    ##    candidates = filter(lambda x: self._contains_distance(x, distance), dependend)
    ##    # determine sources, i.e. clusters created from clusters that do not contain the distance
    ##    sources = Set()
    ##    for c1 in candidates:
    ##        methods = filter(lambda v: isinstance(v, Method), self._graph.ingoing_vertices(c1))
    ##        if len(methods) == 0:
    ##            sources.add(c1)
    ##        elif len(methods) == 1:
    ##            method = methods[0]
    ##            newsource = True
    ##            for c2 in method.inputs():
    ##                if self._contains_distance(c2, distance):
    ##                    newsource = False
    ##                    break
    ##            if newsource:
    ##                sources.add(c1)
    ##        else:
    ##            raise "cluster determined by more than one method"
    ##    diag_print("sources for "+str(distance), "clsolver")
    ##    for source in sources:
    ##        diag_print(str(source), "clsolver")
    ##    # filter sources for dependencies
    ##    #unfiltered = Set(sources)
    ##    #for s1 in unfiltered:
    ##    #    if s1 not in sources: continue
    ##    #    descendants = self._find_descendants(s1)
    ##    #    for s2 in unfiltered:
    ##    #        if s2 not in sources: continue
    ##    #        if s2 in descendants:
    ##    #            sources.remove(s2)
    ##    return sources

    ##def _angle_sources(self, angle):
    ##    # find coincident objects
    ##    dep_a = self._graph.outgoing_vertices(angle.vars[0])
    ##    dep_b = self._graph.outgoing_vertices(angle.vars[1])
    ##    dep_c = self._graph.outgoing_vertices(angle.vars[2])
    ##    dependend = []
    ##    for obj in dep_a:
    ##        if obj in dep_b and obj in dep_c:
    ##            dependend.append(obj)
    ##    candidates = filter(lambda x: self._contains_angle(x, angle), dependend)
    ##    # determine sources, i.e. clusters created from clusters that do not contain the angle
    ##    sources = Set()
    ##    for c1 in candidates:
    ##        methods = filter(lambda v: isinstance(v, Method), self._graph.ingoing_vertices(c1))
    ##        if len(methods) == 0:
    ##            sources.add(c1)
    ##        elif len(methods) == 1:
    ##            method = methods[0]
    ##            newsource = True
    ##            for c2 in method.inputs():
    ##                if self._contains_angle(c2, angle):
    ##                    newsource = False
    ##                    break
    ##            if newsource:
    ##                sources.add(c1)
    ##        else:
    ##            raise "cluster determined by more than one method"
    ##    diag_print("sources for "+str(angle), "clsolver")
    ##    for source in sources:
    ##        diag_print(str(source), "clsolver")
    ##    return sources

    ##def _roots(self,object):
    ##    front = [object]
    ##    result = Set()
    ##    done = Set()
    ##    while len(front) > 0:
    ##        x = front.pop()
    ##        if x not in done:
    ##            done.add(x)
    ##            methods = filter(lambda v: isinstance(v, Method), self._graph.ingoing_vertices(x))
    ##            if len(methods) == 0:
    ##                result.add(x)
    ##            elif len(methods) == 1:
    ##                front += methods[0].inputs()
    ##            else:
    ##                raise "cluster determined by more than one method"
    ##    return result

# class ClusterSolver

