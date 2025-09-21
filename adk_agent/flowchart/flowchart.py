import dash
from dash import html, Input, Output
import dash_cytoscape as cyto
import textwrap

# ---------------------------
# Example structured JSON
# ---------------------------
structured_json = {
    "flowchart": {
        "nodes": [
            {"id": "A", "type": "start", "label": "Lease Agreement Begins", "next": "B"},
            {"id": "B", "type": "decision", "label": "Is it the first day of the month?", "yes": "C", "no": "B"},
            {"id": "C", "type": "process", "label": "Tenant Pays Rent", "next": "D"},
            {"id": "D", "type": "decision", "label": "Rent Paid on Time?", "yes": "E", "no": "F"},
            {"id": "E", "type": "process", "label": "No Late Fee", "next": "G"},
            {"id": "F", "type": "process", "label": "Late Fee of 5% Incurred", "next": "G"},
            {"id": "G", "type": "process", "label": "Landlord Maintains Common Areas", "next": "H"},
            {"id": "H", "type": "decision", "label": "Either Party Wishes to Terminate?", "yes": "I", "no": "K"},
            {"id": "I", "type": "process", "label": "Provide 60-Day Written Notice", "next": "J"},
            {"id": "J", "type": "process", "label": "Tenant Responsible for Rent Obligations Until Termination Date", "next": "L"},
            {"id": "K", "type": "process", "label": "Lease Continues", "next": "B"},
            {"id": "L", "type": "decision", "label": "Tenant Makes Unauthorized Alterations?", "yes": "M", "no": "N"},
            {"id": "M", "type": "process", "label": "Penalties or Lease Termination May Occur", "next": "O"},
            {"id": "N", "type": "process", "label": "No Alteration Penalties", "next": "O"},
            {"id": "O", "type": "decision", "label": "Is there a Dispute?", "yes": "P", "no": "K"},
            {"id": "P", "type": "process", "label": "Dispute Resolved Through Arbitration (Governed by Local Rules)", "next": "K"}
        ],
        "start": "A"
    }
}

# ---------------------------
# Utility: wrap long labels
# ---------------------------
def wrap_label(label, width=20):
    return '\n'.join(textwrap.wrap(label, width))

# ---------------------------
# Convert JSON to Cytoscape elements
# ---------------------------
cyto_elements = []

# Map for nodes
node_map = {node['id']: node for node in structured_json['flowchart']['nodes']}

for node in structured_json['flowchart']['nodes']:
    cyto_elements.append({
        'data': {
            'id': node['id'],
            'label': wrap_label(node['label'], width=20),
            'type': node['type']
        }
    })

# Generate edges dynamically
for node in structured_json['flowchart']['nodes']:
    if node['type'] == 'decision':
        if 'yes' in node:
            cyto_elements.append({'data': {'source': node['id'], 'target': node['yes'], 'label': 'Yes'}})
        if 'no' in node:
            cyto_elements.append({'data': {'source': node['id'], 'target': node['no'], 'label': 'No'}})
    elif 'next' in node:
        cyto_elements.append({'data': {'source': node['id'], 'target': node['next']}})

# ---------------------------
# Dash App
# ---------------------------
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Interactive Legal Flowchart"),
    cyto.Cytoscape(
        id='cytoscape-graph',
        elements=cyto_elements,
        style={'width': '100%', 'height': '800px', 'background-color': '#f7f7f7'},
        layout={'name': 'cose'},
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)',
                    'background-color': '#0074D9',
                    'color': 'white',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'width': '300px',
                    'height': '100px',
                    'shape': 'round-rectangle',
                    'font-size': '14px',
                    'text-wrap': 'wrap'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'curve-style': 'bezier',
                    'target-arrow-shape': 'triangle',
                    'line-color': '#888',
                    'target-arrow-color': '#888',
                    'width': 3,
                    'label': 'data(label)',
                    'font-size': 12,
                    'text-rotation': 'autorotate',
                    'text-background-color': '#fff',
                    'text-background-opacity': 1
                }
            }
        ]
    ),
    html.Div(id='node-info', style={'marginTop': '20px', 'fontSize': '16px'})
])

# ---------------------------
# Callback for node info
# ---------------------------
@app.callback(
    Output('node-info', 'children'),
    Input('cytoscape-graph', 'tapNodeData')
)
def display_node_info(data):
    if data:
        return f"Node: {data['label'].replace(chr(10), ' ')} | Type: {data.get('type', 'Unknown')}"
    return "Click a node to see details."

# ---------------------------
# Run server
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)