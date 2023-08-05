# simple python wrapper for planfact.io API

###resource

planfact API documentation: https://apidoc.planfact.io

###installation

<code>pip install python-planfact</code>

###example usage:

<code>import planfact_api as pf

os.environ["PF_API_KEY"] = *YOUR_API_KEY_HERE*

currencies = pf.get_currencies()</code>