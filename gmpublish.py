#!/usr/bin/env python3

class GmPublish:
	"""Wrapper for the GMPublish program"""

	def __init__(self, addon):
		self.addon = addon

	def create(self):
		"""Upload to the workshop as a new addon"""
		pass

	def update(self, message=None):
		"""Push an update of the addon to the workshop"""
		message = message or addon.getdefault_changelog()

