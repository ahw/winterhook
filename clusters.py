from math import sqrt

def readfile(filename):
    lines = [line for line in file(filename)]

    # First line is the column titles
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # First column in each row is the row name
        rownames.append(p[0])
        # The data for this row is the remainder of the row (i.e., the
        # frequencies of each word.
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data

def pearson(v1, v2):
    # Simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

    # Sums of the squares
    sum1Sq = sum([pow(v,2) for v in v1])
    sum2Sq = sum([pow(v,2) for v in v2])

    # Sum of the products
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt = ((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v2)))
    if den == 0: return 0

    return 1.0 - (num / den)

def hcluster(rows, distfunc = pearson):
    distances = {}
    currentclusterid = -1
    # Clusters are initially just the rows
    clusters = [bicluster(rows[i], id = i) for i in range(len(rows))]

    while len(clusters) > 1:
        # Initialize algorithm by assuming clusters 0 and 1 are the two closest
        lowestpair = (0, 1)
        # Initialize the closest distance value to the distance between
        # clusters 0 and 1.
        closest = distfunc(clusters[0].vec, clusters[1].vec)
        print 'Closest: %s' % closest

        # Loop through every pair looking for the smallest distance
        for i in range(len(clusters)):
            for j in range(i+1, len(clusters)):
                # Distance is the cache of distance calculations. Check if
                # we've already cached the distance between these two
                # clusters. Note that the keys for the distances hash are
                # tuples of cluster ids.
                if (clusters[i].id, clusters[j].id) not in distances:
                    # Compute the distance using whatever "distance"
                    # function is passed in as an argument (Pearson is the
                    # default)
                    distances[(clusters[i].id, clusters[j].id)] = distfunc(clusters[i].vec, clusters[j].vec)

                # Read the distance from the distances hash.
                d = distances[(clusters[i].id, clusters[j].id)]

                if d < closest:
                    # If we have found a distance closer than our
                    # previously-calculated closest distance, then update
                    # the closest distance value and the lowest pair tuple.
                    closest = d
                    lowestpair = (i, j)

        # Calculate the average of the two clusters. Simply average each
        # corresponding pair of of values in their vectors.
        mergevec = [
        (clusters[lowestpair[0]].vec[i] + clusters[lowestpair[1]].vec[i]) / 2.0
        for i in range(len(clusters[0].vec))]

        # Create the new clusters
        newcluster = bicluster(mergevec,
                left = clusters[lowestpair[0]],
                right = clusters[lowestpair[1]],
                distance = closest,
                id = currentclusterid)

        # Decrement the cluster id so we get a new unique cluster id to use
        # next loop around. We're using negative numbers just because we
        # can, and also because cluster ids that weren't in the original set
        # will be negative which helps us keep things straight.
        currentclusterid -= 1

        # Delete the clusters that we just merged.
        del clusters[lowestpair[1]]
        del clusters[lowestpair[0]]

        # Append the newly-merged cluster.
        clusters.append(newcluster)

    # Return the top-level cluster.
    return clusters[0]

def printclust(clust, labels = None, n = 0):
    # Indent to make a hierarchy layout
    for i in range(n): print ' ', # Prevents printing a newline after each space

    if clust.id < 0:
        # By our convention, negative cluster ids indicate that this is a
        # branch node
        print '[%s]---' % n
    else:
        # By our convention, positive ids mean that this is one of the
        # original nodes (an endpoint in the dendrogram)
        if labels == None: print clust.id
        else: print labels[clust.id]

    # Now print the right and left branches
    if clust.left  != None: printclust(clust.left,  labels = labels, n = n+1)
    if clust.right != None: printclust(clust.right, labels = labels, n = n+1)

class bicluster:
    def __init__(self, vec, left = None, right = None, distance = 0.0, id = None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance
