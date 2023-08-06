from parse import parse
from jinja2 import Environment, FileSystemLoader
import os
from datetime import timedelta
from webob import Request, Response


def run(app, host='0.0.0.0', port=5000):
	from waitress import serve
	print(f"Starting server @ http://{host}:{port}/")
	serve(app, host=host, port=port)
	print("Killing server")


class Magicweb:
	def __init__(self, file, frontend_folder="templates"):
		folder = os.path.dirname(file)
		if frontend_folder in os.listdir('.'):
			pass
		else:
			os.chdir(folder)
		self.routes = {}
		self.html = frontend_folder
		self.env = Environment(loader=FileSystemLoader(self.html))
	def set_cookie(self, name, val, resp, max_age=timedelta(days=2), **kwargs):
		resp.set_cookie(name, val, max_age=max_age, **kwargs)
	def delete_cookie(self, name, resp):
		resp.delete_cookie(name)
	def render(self, html_file, response, **kwargs):
		try:
			template = self.env.get_template(html_file)
			content = template.render(**kwargs)
			response.status_code = 200
		except FileNotFoundError:
			content = f'''<h1 style="text-align: center;">404</h1>
			<h3 style="text-align: center;">Template {html_file} not found</h3>'''
			response.status_code = 404
		response.text = content

	def __call__(self, environ, start_response):
		request = Request(environ)

		response = self.handle_request(request)

		return response(environ, start_response)

	def route(self, path):
		assert path not in self.routes, f"Such a route {path} already exists"

		def wrapper(handler):
			self.routes[path] = handler
			return handler

		return wrapper

	def default_response(self, response):
		response.status_code = 404
		response.text = "Not found."

	def find_handler(self, request_path):
		for path, handler in self.routes.items():
			parse_result = parse(path, request_path)
			if parse_result is not None:
				return handler, parse_result.named

		return None, None

	def handle_request(self, request):
		response = Response()

		handler, kwargs = self.find_handler(request_path=request.path)

		if handler is not None:
			handler(request, response, **kwargs)
		else:
			self.default_response(response)

		return response
