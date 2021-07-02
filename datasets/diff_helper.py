import requests
import os
import json
import sys

DATASET_FIELDS = [
  'name',
  'workflow_key',
  'visibility'
]

CATALOGUE_FIELDS = [
  'description',
  'creator',
  'contactPoint',
  'publisher',
  'license',
  'versionInfo',
  'keyword',
  'identifier',
  'rights',
]

DICTIONARY_FIELDS = [
  'name',
  'code',
  'description',
  'fields',
  'lookups'
]

class DiffHelper:
  def toplevel_diff(previous, current):
    diff = {}
    for field in DATASET_FIELDS:
      if (field in current and previous[field] != current[field]): diff[field] = current[field]
    return diff
    
  def catalogue_diff(previous, current):
    diff = {}
    for field in CATALOGUE_FIELDS:
      if (field in current and previous[field] != current[field]): diff[field] = current[field]
    return diff

  def dictionaries_diff(previous, current):
    diff = {}
    codes, dictionaries = DiffHelper.new_and_deleted_dictionaries(previous, current)
    dictionaries += DiffHelper.changed_dictionaries(current, previous, codes)
    return dictionaries

  def dataset_diff(original, data):
    diff = {}

    if original == data: return diff
    
    diff = DiffHelper.toplevel_diff(original, data)
    catalogueUpdates = DiffHelper.catalogue_diff(original['catalogue'], data['catalogue'])
    dictionaryUpdates = DiffHelper.dictionaries_diff(original['dictionaries'], data['dictionaries'])
    if catalogueUpdates: diff['catalogue'] = catalogueUpdates
    if dictionaryUpdates: diff['dictionaries'] = dictionaryUpdates

    return diff

  def sanitize_dict(original):
    modified = original.copy()
    for key in original:
      if key not in DICTIONARY_FIELDS or original[key] == None:
        modified.pop(key)
    return modified

  def new_and_deleted_dictionaries(previous, current):
    dictionaries = []
    currentCodes = [dictionary['code'] for dictionary in current]
    previousCodes = [dictionary['code'] for dictionary in previous]
    newCodes = list(set(currentCodes) - set(previousCodes))
    deletedCodes = list(set(previousCodes) - set(currentCodes))
    for newCode in newCodes:
      dictionaries.append(DiffHelper.find_by_code(current, newCode))
      currentCodes.remove(newCode)
    for deletedCode in deletedCodes:
      dictionary = DiffHelper.find_by_code(previous, deletedCode)
      dictionaries.append({
        'id': dictionary['id'],
        'code': dictionary['code'],
        'toBeDeleted': True
        })
      if deletedCode in currentCodes: currentCodes.remove(deletedCode)
    return [currentCodes, dictionaries]

  def find_by_code(dictionaries, code):
    for dictionary in dictionaries:
      if dictionary['code'] == code:
        return dictionary

  def changed_dictionaries(current, previous, codes):
    dictionaries = []
    for code in codes:
      currentDictionary = DiffHelper.find_by_code(current, code)
      previousDictionary = DiffHelper.find_by_code(previous, code)
      previousDictionary = DiffHelper.sanitize_dict(previousDictionary)
      if currentDictionary == previousDictionary:
        continue

      if currentDictionary.get('fields') != previousDictionary.get('fields') or currentDictionary.get('lookups') != previousDictionary.get('lookups'):
        dictionaries.append(currentDictionary)
      else:
        dictionaries.append({
          'id': currentDictionary.get('id'),
          'code': currentDictionary['code'],
          'name':currentDictionary['name'],
          'description':currentDictionary.get('description'),
        })
    return dictionaries
  