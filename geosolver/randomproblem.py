# ----------- random problem generation ----------------

import random
from diagnostic import diag_print
from geometric import GeometricProblem, DistanceConstraint, AngleConstraint
from intersections import distance_2p, angle_3p
from vector import vector
from tolerance import tol_eq

def _constraint_group(problem, group, dependend, angleratio):
    """Add constraints to problem to constrain given group of points. 
       Group may be optionally dependend on pair of points.
       Creates angle constraints with a given chance."""

    diag_print("_constraint_group(group="+str(group.keys())+",dep="+str(dependend)+")","geometric._constraint_group")
    if len(group) == 2:
        if dependend == None:
           v1 = group.keys()[0]
           v2 = group.keys()[1]
           p1 = group[v1]
           p2 = group[v2]
           dist = distance_2p(p1,p2)
           con = DistanceConstraint(v1,v2,dist)
           diag_print("**Add constraint:"+str(con),"geometric._constraint_group")
           problem.add_constraint(con)
    elif len(group) >= 3:
        # pick three points
        keys = group.keys()
        if dependend == None:
            v1 = random.choice(keys)
        else:
            v1 = dependend[0]
        keys.remove(v1)
        if dependend == None:
            v2 = random.choice(keys)
        else:
            v2 = dependend[1]
        keys.remove(v2)
        v3 = random.choice(keys)
        keys.remove(v3)
        # create three groups
        g = [{},{},{}]
        g[0][v1] = group[v1]
        g[0][v2] = group[v2]
        g[1][v1] = group[v1]
        g[1][v3] = group[v3]
        g[2][v2] = group[v2]
        g[2][v3] = group[v3]
        # distribute remaining points over groups
        while (len(keys) > 0):
            k = keys.pop()
            if dependend == None:
                i = random.randint(0,2)
            else:
                i = random.randint(1,2)
            g[i][k] = group[k]
        # compute facts from prototype
        p1 = group[v1]
        p2 = group[v2]
        p3 = group[v3]
        # group 0: if independend, add at least one independent group
        if dependend == None:
            _constraint_group(problem, g[0], None, angleratio)
        # group 1: random: angle constraint or independend group
        if random.random() > angleratio:
            _constraint_group(problem, g[1], None, angleratio)
        else:
            angle = angle_3p(p1,p2,p3)
            con = AngleConstraint(v1,v2,v3,angle)
            diag_print("**Add constraint:"+str(con),"geometric._constraint_group")
            problem.add_constraint(con)
            _constraint_group(problem, g[1], [v1, v3], angleratio)
        # group 2: random: angle constraint, two configuratins, or independend group
        if random.random() > angleratio:
            _constraint_group(problem, g[2], None, angleratio)
        elif random.random() < 0.5:
            angle = angle_3p(p2,p1,p3)
            con = AngleConstraint(v2,v1,v3,angle)
            diag_print("**Add constraint:"+str(con),"geometric._constraint_group")
            problem.add_constraint(con)
            _constraint_group(problem, g[2], [v2, v3], angleratio)
        else:
            angle = angle_3p(p2,p3,p1)
            con = AngleConstraint(v2,v3,v1,angle)
            diag_print("**Add constraint:"+str(con),"geometric._constraint_group")
            problem.add_constraint(con)
            _constraint_group(problem, g[2], [v2, v3], angleratio)

def _round(val,roundoff):
    if roundoff > 0:
        return val - (val % roundoff)
    else:
        return val

def random_problem_2D(numpoints, radius=10.0, roundoff=0.0, angleratio=0.5):
    """Generate a random problem with given number of points, a roundoff
       value for the prototype points, a radius for the cloud of prototype points
       and a ratio of angle constraints over distance constraints"""
    group = {}
    problem = GeometricProblem(dimension=2)
    i = 0
    while i < numpoints:
        aname = 'p'+str(i)
        apoint = vector([
            _round(random.uniform(-radius,radius),roundoff),
            _round(random.uniform(-radius,radius),roundoff)
        ])
        unique = True
        for v in group:
            p = group[v]
            if tol_eq(apoint[0],p[0]) and tol_eq(apoint[1],p[1]):
                unique = False
                break
        if unique:
                problem.add_point(aname, apoint)
                group[aname] = apoint
                i = i + 1
    #next
    _constraint_group(problem, group, None, angleratio)
    return problem


def add_random_constraint(problem, ratio):
    """add a random constraint to a problem, with a given ratio angles/distances"""
    if random.random() < ratio:   
        # add angle
        pointvars = list(problem.cg.variables())
        random.shuffle(pointvars)
        v1 = pointvars[0]
        v2 = pointvars[1]
        v3 = pointvars[2]
        p1 = problem.get_point(v1)
        p2 = problem.get_point(v2)
        p3 = problem.get_point(v3)
        angle = angle_3p(p1,p2,p3)
        con = AngleConstraint(v1,v2,v3,angle)
        diag_print("**Add constraint:"+str(con),"drplan")
        problem.add_constraint(con)
    else:
        # add distance
        pointvars = list(problem.cg.variables())
        random.shuffle(pointvars)
        v1 = pointvars[0]
        v2 = pointvars[1]
        p1 = problem.get_point(v1)
        p2 = problem.get_point(v2)
        dist = distance_2p(p1,p2)
        con = DistanceConstraint(v1,v2,dist)
        diag_print("**Add constraint:"+str(con),"drplan")
        problem.add_constraint(con)
    return

def randomize_angles(problem):
    randomize_balloons(problem)
    randomize_hedgehogs(problem)
    randomize_balloons(problem)
    randomize_hedgehogs(problem)
    return problem

def randomize_hedgehogs(problem):
    """combine adjacent angles to hedgehogs and replace with different angles.
       modifies problem
    """
    assert problem.dimension == 2
    angles = filter(lambda c: isinstance(c, AngleConstraint), problem.cg.constraints())
    hogs = set()
    # make hogs from angles
    for angle in angles:
        vars = angle.variables()
        hog = (vars[1],frozenset([vars[0],vars[2]]))
        hogs.add(hog)
        # REMOVE CONSTRAINT
        problem.rem_constraint(angle)

    # combine hogs
    queue = list(hogs)
    while len(queue)>0:
        hog1 = queue.pop()
        if hog1 not in hogs:
            continue
        cvar1 = hog1[0]
        xvars1 = hog1[1]
        for hog2 in hogs:
            if hog1 == hog2:
                continue
            cvar2 = hog2[0]
            xvars2 = hog2[1]
            if cvar1 == cvar2: 
                shared = xvars1.intersection(xvars2)
                if len(shared) > 0:
                    hogs.remove(hog1)
                    hogs.remove(hog2)
                    newhog = (cvar1, xvars1.union(xvars2))
                    hogs.add(newhog)
                    queue.append(newhog)
                    break
    
    # rewrite hogs
    for hog in hogs:
        cvar = hog[0]
        xvars = hog[1]
        varlist = list(xvars)
        random.shuffle(varlist)
        for i in range(1, len(varlist)): 
            v1 = varlist[i-1] 
            v2 = cvar 
            v3 = varlist[i]
            # ADD CONSTRAINT
            problem.add_constraint(AngleConstraint(v1,v2,v3, 
                angle_3p(problem.get_point(v1), problem.get_point(v2), problem.get_point(v3))
            ))

    return problem
# def randomize_hedgehogs

def randomize_balloons(problem):
    """combine adjacent angles to balloons and replace with different angles.
       modifies problem
    """
    assert problem.dimension == 2
    angles = filter(lambda c: isinstance(c, AngleConstraint), problem.cg.constraints())
    balloons = set()
    toremove = set()
    # make hogs from angles
    for angle1 in angles:
        cvar1 = angle1.variables()[1]
        for angle2 in angles:
            if angle2 == angle1: continue
            cvar2 = angle2.variables()[1]
            if cvar1 == cvar2: continue
            shared = set(angle1.variables()).intersection(angle2.variables())
            if len(shared) == 3: 
                balloon = frozenset(angle1.variables())
                balloons.add(balloon)
                toremove.add(angle1)
                toremove.add(angle2)

    # remove constraints
    for con in toremove:
        problem.rem_constraint(con)

    print "initial balloons", balloons

    # combine balloons
    queue = list(balloons)
    while len(queue)>0:
        bal1 = queue.pop()
        if bal1 not in balloons:
            continue
        for bal2 in balloons:
            if bal1 == bal2:
                continue
            shared = bal1.intersection(bal2)
            if len(shared) >= 2:
                balloons.remove(bal1)
                balloons.remove(bal2)
                newbal= (bal1.union(bal2))
                balloons.add(newbal)
                queue.append(newbal)
                break
    
    print "combined balloons", balloons

    # rewrite balloons
    for bal in balloons:
        # constrain first three points
        vars = list(bal)
        random.shuffle(vars)
        for i in range(2, len(vars)):
            lvars = vars[i-2:i+1]
            random.shuffle(lvars)
            problem.add_constraint(AngleConstraint(lvars[0],lvars[1],lvars[2], 
                angle_3p(problem.get_point(lvars[0]), problem.get_point(lvars[1]), problem.get_point(lvars[2]))
            ))
            problem.add_constraint(AngleConstraint(lvars[1],lvars[2],lvars[0], 
                angle_3p(problem.get_point(lvars[1]), problem.get_point(lvars[2]), problem.get_point(lvars[0]))
            ))

    return problem


def random_distance_problem_3D(npoints, radius, roundoff):
	"""creates a 3D problem with random distances"""
	problem = GeometricProblem(dimension=3)
	for i in range(npoints):
		# add point
		newvar = 'v'+str(i)
		newpoint = vector([
            _round(random.uniform(-radius,radius),roundoff),
            _round(random.uniform(-radius,radius),roundoff),
            _round(random.uniform(-radius,radius),roundoff)
        ])
		sellist = list(problem.cg.variables())
		problem.add_point(newvar, newpoint)
		# add distance constraints    
		for j in range(min(3,len(sellist))):
			index = random.randint(0,len(sellist)-1)
			var = sellist.pop(index)
			point = problem.get_point(var)
			dist = distance_2p(point,newpoint)
			problem.add_constraint(DistanceConstraint(var,newvar,dist))
	return problem

def random_triangular_problem_3D(npoints, radius, roundoff, pangle):
	problem = random_distance_problem_3D(npoints, radius, roundoff)
	points = problem.cg.variables()	
	triangles = []
	for i1 in range(len(points)):
		for i2 in range(i1+1,len(points)):
			for i3 in range(i2+1,len(points)):	
				p1 = points[i1]
				p2 = points[i2]
				p3 = points[i3]
				if (problem.get_distance(p1,p2) and
				    problem.get_distance(p1,p3) and
					problem.get_distance(p2,p3)):
					triangles.append((p1,p2,p3))
	for tri in triangles:
		for i in range(2):
				p = tri[i]
				pl = tri[(i+1)%3]
				pr = tri[(i+2)%3]
				if problem.get_distance(pl,pr) and random.random() < pangle:
					problem.rem_constraint(problem.get_distance(pl,pr))
					angle = angle_3p(problem.get_point(pl),
				                 problem.get_point(p),
				                 problem.get_point(pr))
					problem.add_constraint(AngleConstraint(pl,p,pr,angle))
	return problem	


def test():
	#problem = random_triangular_problem_3D(10, 10.0, 0.0, 0.5)
	problem = random_problem_2D(10, 10.0, 0.0, 0.6)
        problem = randomize_angles(problem)
	print problem

if __name__ == "__main__": test()

