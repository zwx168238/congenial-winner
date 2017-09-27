#!/usr/bin/env python
# -*- coding=UTF-8 -*-

from optparse import OptionParser
from xml.etree.ElementTree import ElementTree

def generate_default_xml(xml_input, xml_output, prefix, gerrit_url):
	input_tree = ElementTree(file=xml_input)
   	input_root = input_tree.getroot()
	for child in input_root:
		if (child.tag == "remote"):
			if child.attrib.has_key("name"):
				tmp_name = child.attrib["name"]
				tmp_fetch = child.attrib["fetch"]
				tmp_review = child.attrib["review"]
				#print child.attrib["name"]
				real_name = tmp_name.replace(tmp_name, "orgin")
				real_fetch = tmp_fetch.replace(tmp_fetch, "..")
				real_review = tmp_review.replace(tmp_review, gerrit_url)
				child.set("name", real_name)
				child.set("fetch", real_fetch)
				child.set("review", real_review)
				continue
		if (child.tag == "default"):
			if child.attrib.has_key("remote"):
				tmp_remote = child.attrib["remote"]
				tmp_revision = child.attrib["revision"]
				tmp_sync = child.attrib["sync-j"]
				#print child.attrib["remote"]
				real_remote = tmp_remote.replace(tmp_remote, "orgin")
				real_revision = tmp_revision.replace(tmp_revision, "master")
				real_sync= tmp_sync.replace(tmp_sync, "4")
				child.set("remote", real_remote)
				child.set("revision", real_revision)
				child.set("sync-j", real_sync)
				continue
		if (child.tag == "project"):
			print child.attrib["name"]
			if child.attrib.has_key("name"):
				tmp_name = child.attrib["name"]
				real_name = prefix + '/'+ tmp_name
				child.set("name", real_name)
				continue
			if child.attrib.has_key("revision"):
				del child.attrib["revision"]
				continue
			if child.attrib.has_key("remote"):
				del child.attrib["remote"]
				continue
			if child.attrib.has_key("groups"):
				del child.attrib["groups"]
				continue
			if child.attrib.has_key("upstream"):
				del child.attrib["upstream"]
				continue
#write to file
	input_tree.write(xml_output, 'UTF-8')

def add_path(xml_input, xml_output):
	aosp_tree = ElementTree(file=xml_input)
   	aosp_root = aosp_tree.getroot()
	for child in aosp_root:
		if (child.tag == "project"):
			if child.attrib.has_key("path"):
				print child.attrib["name"]
				tmp_path = child.attrib["path"]
				real_path = "LINUX/android/" + tmp_path
				child.set("path", real_path)
				continue
#write to file
	aosp_tree.write(xml_output, 'UTF-8')

def modify_name(xml_input, xml_output):
	aosp_tree = ElementTree(file=xml_input)
   	aosp_root = aosp_tree.getroot()
	for child in aosp_root:
		if (child.tag == "project"):
			if child.attrib.has_key("name"):
				tmp_name = child.attrib["name"]
				real_name = prefix + tmp_name
				child.set("name", real_name)
				continue
#write to file
	aosp_tree.write(xml_output, 'UTF-8')

def modify(xml_input, xml_output,key,value):
	aosp_tree = ElementTree(file=xml_input)
   	aosp_root = aosp_tree.getroot()
	for child in aosp_root:
		if (child.tag == "project"):
			if child.attrib.has_key("key"):
				tmp_key = child.attrib["key"]
				#print child.attrib["key"]
				if tmp_key.startswith("value"):
					real_key = tmp_key[5:]
					#print "real_key= " + real_key
					print real_key
					child.set("key", real_key)
					continue
			else:
				print "has not this key,pls check by hand"
				continue
#write to file

def remove(xml_input, xml_output,paramerer):
	tree = ElementTree(file=xml_input)
	root = tree.getroot()

	for child in root:
		if (child.tag == "project"):
			print child.attrib["name"]
			if child.attrib.has_key("paramerer"):
				del child.attrib["paramerer"]
	tree.write(xml_output, 'UTF-8')


def main():
	usage = "usage: %prog [options] arg"
	parser = OptionParser(usage)
	parser.add_option("-i", "--in_file", dest="xml_input",
						help="xml input file")
	parser.add_option("-r", "--remot", dest="remote_name",
						help="manifest xml remote which you want set")
	parser.add_option("-o", "--out_file", dest="xml_output",
						help="xml output file")
	parser.add_option("-p", "--prefix", dest="PREFIX",
						help="prefix the same as parent pro name")
	parser.add_option("-u", "--url", dest="GERRIT_URL",default="http://192.168.65.151:8071/" ,
						help="gerrit url")
	parser.add_option("-t", "--type", dest="mig_type",
						help="'del_revision' means delete revision"
						"'del_groups' means delete groups"
						"'del_upstream' means delete upstream"
						"'modify_groups' means modify groups"
						"'modify_name' means modify name"
						"'add_path' means modify path"
						"'manifest' means generate_default_xml")

	(options, args) = parser.parse_args()
	if options.mig_type == "del_revision":
		remove_revision(options.xml_input, options.xml_output);
	elif options.mig_type == "del_groups":
		remove_groups(options.xml_input, options.xml_output);
	elif options.mig_type == "del_upstream":
		remove_upstream(options.xml_input, options.xml_output);
	elif options.mig_type == "del_remote":
		remove_remote(options.xml_input, options.xml_output);
	elif options.mig_type == "modify_groups":
		modify_groups(options.xml_input, options.xml_output);
	elif options.mig_type == "modify_name":
		modify_name(options.xml_input, options.xml_output);
	elif options.mig_type == "modify_path":
		modify_path(options.xml_input, options.xml_output);
	elif options.mig_type == "add_path":
		add_path(options.xml_input, options.xml_output);
	elif options.mig_type == "remove":
		remove(options.xml_input, options.xml_output,options.paramerer);
	elif options.mig_type == "manifest":
		generate_default_xml(options.xml_input, options.xml_output, options.PREFIX, options.GERRIT_URL);
if __name__ == "__main__":
	main()
