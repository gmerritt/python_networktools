#!/usr/bin/env python

import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


tree = ET.parse('lankershim_controller.xml')
oldset = tree.getroot()




controller_dict = {}
for oldcontroller in oldset.iter('controller'):
  plan_dict = {}
  plan_list = oldcontroller.find('PlanList')
  for plan in plan_list:
    plan_id = plan.attrib['id']
    plan_dict[plan_id]={}
    plan_dict[plan_id]['cycle_length']=plan.attrib['cyclelength']
    intersection = plan.find('intersection')
    plan_dict[plan_id]['offset']=intersection.attrib['offset']
    plan_stages = []
    for stage in intersection.iter('stage'):
      A=stage.attrib['movA']
      if 'movB' in stage.attrib:
        B=stage.attrib['movB']
      else:
        B='0'
      plan_stages.append({'A':A, 'B':B, 'green_time':stage.attrib['greentime']})
    plan_dict[plan_id]['stages']=plan_stages
  NODE_ID=intersection.attrib['node_id'] #this should be the same for all plans in one controller object...
  plan_seq = oldcontroller.find('PlanSequence')
  # transition_delay = plan_seq.attrib['transition_delay']
  for plan_ref in plan_seq.iter('plan_reference'):
    plan_dict[plan_ref.attrib['plan_id']]['start_time']=plan_ref.attrib['start_time']
  controller_dict[NODE_ID]=plan_dict




newset = ET.Element('ControllerSet')
newset.attrib['id']='-1'
newset.attrib['project_id']='-1'

for node_id in controller_dict.keys():

  controller = ET.SubElement(newset, 'controller')
  controller.attrib['id'] = node_id
  controller.attrib['dt'] = '1'
  controller.attrib['name']='lankershim_'+node_id.strip('-')
  controller.attrib['type']='SIG_Pretimed'
  controller.attrib['enabled']='true'

  params = ET.SubElement(controller, 'parameters')
  p = ET.SubElement(params, 'parameter')
  p.attrib['name']='Transition Delay'
  p.attrib['value']='0'

  targets = ET.SubElement(controller, 'target_actuators')
  t = ET.SubElement(targets, 'target_actuator')
  t.attrib['id']=node_id.strip('-')
  t.attrib['usage']='signal'

  #input cycle lengths
  cycle_length = ET.SubElement(controller, 'table')
  cycle_length.attrib['name']='Cycle Length'
  columns_cycle = ET.SubElement(cycle_length, 'column_names')
  c1 = ET.SubElement(columns_cycle, 'column_name')
  c1.attrib = {'id':'0', 'key':'false', 'name':'Plan ID'}
  c2 = ET.SubElement(columns_cycle, 'column_name')
  c2.attrib = {'id':'1', 'key':'false', 'name':'Cycle Length'}
  for pid,plan in controller_dict[node_id].iteritems():
    row = ET.SubElement(cycle_length,'row')
    id_col = ET.SubElement(row, 'column')
    id_col.attrib = {'id':'0'}
    id_col.text = pid
    cycle_col = ET.SubElement(row, 'column')
    cycle_col.attrib = {'id':'1'}
    cycle_col.text = plan['cycle_length']

  #input offsets
  offsets = ET.SubElement(controller, 'table')
  offsets.attrib['name']='Offsets'
  columns_offset = ET.SubElement(offsets, 'column_names')
  o1 = ET.SubElement(columns_offset, 'column_name')
  o1.attrib = {'id':'0', 'key':'false', 'name':'Plan ID'}
  o2 = ET.SubElement(columns_offset, 'column_name')
  o2.attrib = {'id':'1', 'key':'false', 'name':'Signal'}
  o3 = ET.SubElement(columns_offset, 'column_name')
  o3.attrib = {'id':'2', 'key':'false', 'name':'Offset'}
  for pid,plan in controller_dict[node_id].iteritems():
    row = ET.SubElement(offsets,'row')
    id_col = ET.SubElement(row, 'column')
    id_col.attrib = {'id':'0'}
    id_col.text = pid
    signal_col = ET.SubElement(row, 'column')
    signal_col.attrib = {'id':'1'}
    signal_col.text = node_id.strip('-')
    offset_col = ET.SubElement(row, 'column')
    offset_col.attrib={'id':'2'}
    offset_col.text = plan['offset']

  #input plan lists
  plan_list = ET.SubElement(controller, 'table')
  plan_list.attrib['name']='Plan List'
  columns_pl = ET.SubElement(plan_list, 'column_names')
  l1 = ET.SubElement(columns_pl, 'column_name')
  l1.attrib = {'id':'0', 'key':'false', 'name':'Plan ID'}
  l2 = ET.SubElement(columns_pl, 'column_name')
  l2.attrib = {'id':'1', 'key':'false', 'name':'Signal'}
  l3 = ET.SubElement(columns_pl, 'column_name')
  l3.attrib = {'id':'2', 'key':'false', 'name':'Movement A'}
  l4 = ET.SubElement(columns_pl, 'column_name')
  l4.attrib = {'id':'3', 'key':'false', 'name':'Movement B'}
  l5 = ET.SubElement(columns_pl, 'column_name')
  l5.attrib = {'id':'4', 'key':'false', 'name':'Green Time'}
  for pid,plan in controller_dict[node_id].iteritems():
    for stage in plan['stages']:
      row = ET.SubElement(plan_list, 'row')
      id_col = ET.SubElement(row, 'column')
      id_col.attrib = {'id':'0'}
      id_col.text = pid
      signal_col = ET.SubElement(row, 'column')
      signal_col.attrib = {'id':'1'}
      signal_col.text = node_id.strip('-')
      movA_col = ET.SubElement(row, 'column')
      movA_col.attrib = {'id':'2'}
      movA_col.text = stage['A']
      movB_col = ET.SubElement(row, 'column')
      movB_col.attrib = {'id':'3'}
      movB_col.text = stage['B']
      green_col = ET.SubElement(row, 'column')
      green_col.attrib = {'id':'4'}
      green_col.text = stage['green_time']

  #input plan sequences
  plan_sequence = ET.SubElement(controller, 'table')
  plan_sequence.attrib['name']='Plan Sequence'
  columns_ps = ET.SubElement(plan_sequence, 'column_names')
  s1 = ET.SubElement(columns_ps, 'column_name')
  s1.attrib = {'id':'0', 'key':'false', 'name':'Plan ID'}
  s2 = ET.SubElement(columns_ps, 'column_name')
  s2.attrib = {'id':'1', 'key':'false', 'name':'Start Time'}
  for pid,plan in controller_dict[node_id].iteritems():
    row = ET.SubElement(plan_sequence,'row')
    id_col = ET.SubElement(row, 'column')
    id_col.attrib = {'id':'0'}
    id_col.text = pid
    start_col = ET.SubElement(row, 'column')
    start_col.attrib = {'id':'1'}
    if 'start_time' in plan:
      start_col.text = plan['start_time']
    else: start_col.text = '-1'

  # oldsequence=oldcontroller.find('PlanSequence')
  # for plan_reference in oldsequence.iter('plan_reference'):
  #   newrow = ET.SubElement(plan_sequence, 'row')
  #   idcol = ET.SubElement(newrow, 'column')
  #   idcol.attrib['id'] = "0"
  #   idcol.text = str(plan_reference.attrib['plan_id'])
  #   startcol = ET.SubElement(newrow, 'column')
  #   startcol.attrib['id']='1'
  #   startcol.text = plan_reference.attrib['start_time']
  #
  # oldlist=oldcontroller.find('PlanList')
  # for plan in oldsequence.iter('plan'):
  #   newrow = ET.SubElement(plan_sequence, 'row')
  #   idcol = ET.SubElement(newrow, 'column')
  #   idcol.attrib['id'] = "0"
  #   idcol.text = str(plan_reference.attrib['id'])
  #   sigcol = ET.SubElement(newrow, 'column')
  #   sigcol.attrib['id']='1'
  #   sigcol.text = plan_reference.attrib['start_time']

tree = ET.ElementTree(newset)
tree.write("reformatted_controller.xml")
#
#
# rough_string = ET.tostring(newset, 'utf-8')
# reparsed = minidom.parseString(rough_string)
# print(reparsed.toprettyxml(indent="\t"))
