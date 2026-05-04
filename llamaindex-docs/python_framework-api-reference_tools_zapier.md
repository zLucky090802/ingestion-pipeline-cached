# Zapier
Init file.
##  ZapierToolSpec [#](https://developers.llamaindex.ai/python/framework-api-reference/tools/zapier/#llama_index.tools.zapier.ZapierToolSpec "Permanent link")
Bases: 
Zapier tool spec.
Source code in `llama-index-integrations/tools/llama-index-tools-zapier/llama_index/tools/zapier/base.py`  
| 
```
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
```
 | 
```
classZapierToolSpec(BaseToolSpec):
"""Zapier tool spec."""

    spec_functions = []

    def__init__(
        self, api_key: Optional[str] = None, oauth_access_token: Optional[str] = None
    ) -> None:
"""Initialize with parameters."""
        if api_key:
            self._headers = {"x-api-key": api_key}
        elif oauth_access_token:
            self._headers = {"Authorization": f"Bearer {oauth_access_token}"}
        else:
            raise ValueError("Must provide either api_key or oauth_access_token")

        # Get the exposed actions from Zapier
        actions = json.loads(self.list_actions())
        if "results" not in actions:
            raise ValueError(
                "No Zapier actions exposed, visit https://nla.zapier.com/dev/actions/"
                " to expose actions."
            )
        results = actions["results"]

        # Register the actions as Tools
        for action in results:
            params = action["params"]

            deffunction_action(id=action["id"], **kwargs):
                return self.natural_language_query(id, **kwargs)

            action_name = action["description"].split(": ")[1].replace(" ", "_")
            function_action.__name__ = action_name
            function_action.__doc__ = f"""
                This is a Zapier Natural Language Action function wrapper.

                The 'instructions' key is REQUIRED for all function calls.
                The instructions key is a natural language string describing the action to be taken
                The following are all of the valid arguments you can provide: {params}

                Ignore the id field, it is provided for you.
                If the returned error field is not null, interpret the error and try to fix it. Otherwise, inform the user of how they might fix it.

            setattr(self, action_name, function_action)
            self.spec_functions.append(action_name)

    deflist_actions(self):
        response = requests.get(
            "https://nla.zapier.com/api/v1/dynamic/exposed/", headers=self._headers
        )
        return response.text

    defnatural_language_query(self, id: str, **kwargs):
        response = requests.post(
            ACTION_URL_TMPL.format(action_id=id),
            headers=self._headers,
            data=json.dumps(kwargs),
        )
        return response.text

```
 |  
| --- | --- |  
options: members: - ZapierToolSpec
