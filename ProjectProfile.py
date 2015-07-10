#encoding: utf-8

import sublime, sublime_plugin
import os	


class ProjectProfileHelper:
	"""
	Helper class.
	"""

	def active_view():
		"""
		Get active view of current window
		"""
		return sublime.Window.active_view(sublime.active_window())

	def get_profile(name):
		"""
		Get profile by name (or None)
		"""
		settings = sublime.load_settings("ProjectProfile.sublime-settings")
		profiles = settings.get('profiles')
		if profiles is None:
			return None
		if not profiles.get(name) is None:
			return profiles[name]
		return None

	def profile_name():
		"""
		Get current project profile name (or None)
		"""
		view = ProjectProfileHelper.active_view()
		project_data = view.window().project_data()
		if project_data is None:
			return None
		if "profile" not in project_data:
			return None
		return project_data["profile"]

	def get_all_packages():
		"""
		Get all installed packages list
		"""
		paths = [sublime.installed_packages_path(), sublime.packages_path()]
		result = []
		for path in paths:
			content = os.listdir(path)
			for item in content:
				full_path = os.path.join(path, item)
				# Check, is file a right package
				if os.path.isdir(full_path):
					result.append(item)
				else:
					ext = item.split('.')[-1].lower()
					if ext=="sublime-package":
						#TODO: Use other method
						result.append(item.replace(".sublime-package", ""))
		return result

	def get_user_disabled():
		"""
		Get manually disable packages list from 'disabled_packages' or 'ignored_packages'.
		We change 'ignored_packages', so we can't use it generally
		"""
		global_settings = sublime.load_settings("Preferences.sublime-settings")
		result = global_settings.get("disabled_packages")
		if result is None:
			result = global_settings.get("ignored_packages")
			global_settings.set("disabled_packages", result)
		return result

	def get_always_run_packages():
		"""
		Get list of packages that can't be disabled
		"""
		settings = sublime.load_settings("ProjectProfile.sublime-settings")
		result = settings.get("always") 
		if result is None:
			result = []
		return result

	def set_packages(packages):
		"""
		Leave only packages from packages array enabled
		"""
		global_settings = sublime.load_settings("Preferences.sublime-settings")
		to_disable = ProjectProfileHelper.get_user_disabled()
		for package in ProjectProfileHelper.get_all_packages():
			if (not package in packages) and (not package in to_disable):
				to_disable.append(package)
		print("Try to disable packages", to_disable)
		global_settings.set("ignored_packages", to_disable)

	def initialize_profile(name):
		"""
		Work with selected profile.
		"""
		print("Initializing profile " + name)
		profile = ProjectProfileHelper.get_profile(name)
		if profile is None:
			print("Profile " + name + " does not configured.")
			return
		packages = profile.get("packages")
		if "ProjectProfile" not in packages:
			packages.append("ProjectProfile")
		if "User" not in packages:
			packages.append("User")
		ProjectProfileHelper.set_packages(packages + ProjectProfileHelper.get_always_run_packages())

	def free():
		"""
		Enable all packages not listed as disabled
		"""
		disabled = ProjectProfileHelper.get_user_disabled()
		global_settings = sublime.load_settings("Preferences.sublime-settings")
		global_settings.set("ignored_packages", disabled)	



#TODO : Detect project opening/swtching
class ProjectProfile(sublime_plugin.EventListener):
	active_profile = None

	def __init__(self, *args, **kwargs):
		super(ProjectProfile, self).__init__(*args, **kwargs)
		profile = ProjectProfileHelper.profile_name()
		if not profile is None:
			ProjectProfileHelper.initialize_profile(profile)
		else:
			ProjectProfileHelper.free()

	def set_profile(name):
		if ProjectProfile.active_profile!=name:
			ProjectProfile.active_profile = name
			ProjectProfileHelper.initialize_profile(name)

	def use_views_profile(view):
		profile = ProjectProfileHelper.profile_name()
		if profile is None:
			return
		else:
			ProjectProfile.active_profile = None
			ProjectProfileHelper.free()
		ProjectProfile.set_profile(profile)

	def on_new(self, view):
		ProjectProfile.use_views_profile(view)

	def on_load(self, view):
		ProjectProfile.use_views_profile(view)

	def on_post_save(self, view):
		ProjectProfile.use_views_profile(view)