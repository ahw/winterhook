#!/usr/bin/python

import generatefeedvector
import clusters

# Reads feedlist.txt and writes output to blogdata.txt
generatefeedvector.buildblogdata()

blognames, words, data = clusters.readfile('blogdata.txt')
clust = clusters.hcluster(data)
clusters.printclust(clust, labels = blognames)
