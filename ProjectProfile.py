#encoding: utf-8

import sublime, sublime_plugin
import os

#TODO : Detect project opening/swtching
class ProjectProfile(sublime_plugin.EventListener):
	view_profiles = {}


	def view_profile(self, view):
		window = view.window()
		project_data = window.project_data()
		if not project_data is None:
			project_type = project_data['profile']
			return project_type
		else:
			return None


	def get_packages(self):
		packages = os.listdir(sublime.packages_path())
		installed_packages = os.listdir(sublime.installed_packages_path())
		packages += [os.path.splitext(package)[0] for package in installed_packages]
		return packages


	def profile_packages(self, profile):
		def get_profile_packages(settings, name, scanned = []):
			if name in scanned:
				return []
			package_list = settings.get("profiles").get(name)
			if package_list is None:
				package_list = []
			extends = settings.get("profiles_extends")[profile]
			if not extends is None:
				for item in extends:
					package_list += get_profile_packages(settings, item, scanned + [name])
			return package_list

		settings = sublime.load_settings("ProjectProfile.sublime-settings")
		always_enabled_packages = settings.get("always")
		profile_packages = get_profile_packages(settings, profile)
		return always_enabled_packages + profile_packages


	def disable_packages(self, packages):
		print("ProjectProfile : disabling " + str(packages))
		settings = sublime.load_settings("Preferences.sublime-settings")
		settings.set("ignored_packages", packages)
		sublime.save_settings("Preferences.sublime-settings")


	def switch_profile(self, name):
		if not name is None:
			enabled_packages = self.profile_packages(name)
			if not 'ProjectProfile' in enabled_packages:
				enabled_packages.append('ProjectProfile')
			all_packages = self.get_packages()
			ignored_packages = list(set(all_packages) - set(enabled_packages))
			self.disable_packages(ignored_packages)


	def view_active_profile(self, view):
		if not view.id() in ProjectProfile.view_profiles.keys():
			return None
		return ProjectProfile.view_profiles[view.id()]


	def use_view_profile(self, view):
		profile = self.view_profile(view)
		current = self.view_active_profile(view)
		if (profile != current) and (not profile is None):
			self.switch_profile(profile)
			ProjectProfile.view_profiles[view.id()] = profile


	def init_callback(self):
		view = sublime.active_window().active_view()
		self.use_view_profile(view)

	def __init__(self, *args, **kwargs):
		super(ProjectProfile, self).__init__(*args, **kwargs)
		print ("ProjectProfile : __init__")
		# I can't run it generally, because I must disable plugins only after start
		sublime.set_timeout(lambda: self.init_callback(), 1000)


	def on_load(self, view):
		print ("ProjectProfile : on_load")
		self.use_view_profile(view)


	def on_pre_save(self, view):
		print("ProjectProfile : on_pre_save")
		self.use_view_profile(view)


	def on_new(self, view):
		print("ProjectProfile : on_new")
		self.use_view_profile(view)