import dash
from dash import html, Input, Output
import dash_cytoscape as cyto

# ---------------------------
# Example structured JSON
# ---------------------------
structured_json = {
  "contract_flowchart": {
    "nodes": [
      {"id": "A", "type": "start", "label": "Start"},
      {"id": "B", "type": "obligation", "label": "Service Provider Obligation: Deliver Software & Documentation within 30 days"},
      {"id": "B1", "type": "risk_assessment", "label": "Risk: Delays in Delivery?"},
      {"id": "B2", "type": "consequence", "label": "Consequences: Project Timeline Disruption, Potential Penalty Fees"},
      {"id": "C", "type": "obligation", "label": "Client Obligation: Provide Timely Access, Data & Resources"},
      {"id": "C1", "type": "risk_assessment", "label": "Risk: Failure to provide Timely Access, Data & Resources?"},
      {"id": "C2", "type": "consequence", "label": "Consequences: Project Delays, Additional Costs, Potential Disputes"},
      {"id": "D", "type": "obligation", "label": "Mutual Obligation: Maintain Confidentiality"},
      {"id": "D1", "type": "risk_assessment", "label": "Risk: Breach of Confidentiality?"},
      {"id": "D2", "type": "consequence", "label": "Consequences: Legal Action, Financial Liability, Reputational Harm"},
      {"id": "E", "type": "obligation", "label": "Intellectual Property: IP Remains with Provider until Full Payment"},
      {"id": "E1", "type": "risk_assessment", "label": "Risk: Non-Payment by Client?"},
      {"id": "E2", "type": "consequence", "label": "Consequences: Ownership Disputes, Project Interruptions"},
      {"id": "F", "type": "obligation", "label": "Termination Clause: Either Party may Terminate with Written Notice"},
      {"id": "F1", "type": "risk_assessment", "label": "Risk: Improper Termination?"},
      {"id": "F2", "type": "consequence", "label": "Consequences: Claims for Damages, Enforceability Issues"},
      {"id": "G", "type": "success", "label": "Contract Fulfilled"},
      {"id": "H", "type": "end", "label": "End"}
    ],
    "edges": [
      {"source": "A", "target": "B"},
      {"source": "B", "target": "B1"},
      {"source": "B1", "target": "B2", "condition": "Yes"},
      {"source": "B1", "target": "C", "condition": "No"},
      {"source": "B2", "target": "H"},
      {"source": "C", "target": "C1"},
      {"source": "C1", "target": "C2", "condition": "Yes"},
      {"source": "C1", "target": "D", "condition": "No"},
      {"source": "C2", "target": "H"},
      {"source": "D", "target": "D1"},
      {"source": "D1", "target": "D2", "condition": "Yes"},
      {"source": "D1", "target": "E", "condition": "No"},
      {"source": "D2", "target": "H"},
      {"source": "E", "target": "E1"},
      {"source": "E1", "target": "E2", "condition": "Yes"},
      {"source": "E1", "target": "F", "condition": "No"},
      {"source": "E2", "target": "H"},
      {"source": "F", "target": "F1"},
      {"source": "F1", "target": "F2", "condition": "Yes"},
      {"source": "F1", "target": "G", "condition": "No"},
      {"source": "F2", "target": "H"},
      {"source": "G", "target": "H"}
    ]
  }
}

# ---------------------------
# Convert JSON to Cytoscape elements
# ---------------------------
cyto_elements = []

for clause in structured_json['clauses']:
    cyto_elements.append({
        'data': {
            'id': clause['clause_id'],
            'label': clause['summary'],
            'risk': clause.get('risk', 'Not defined')  # Safe access
        }
    })

for edge in structured_json['edges']:
    cyto_elements.append({
        'data': {
            'source': edge['source'],
            'target': edge['target']
        }
    })

# ---------------------------
# Risk color map
# ---------------------------
risk_color_map = {
    "low": "#2ECC40",         # green
    "medium": "#FFDC00",      # yellow
    "high": "#FF4136",        # red
    "Not defined": "#AAAAAA"  # gray for missing risk
}

# Assign colors to nodes
for element in cyto_elements:
    if 'risk' in element['data']:
        element['data']['risk_color'] = risk_color_map.get(element['data']['risk'], "#AAAAAA")

# ---------------------------
# Dash App
# ---------------------------
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Interactive Legal Flowchart"),
    cyto.Cytoscape(
        id='cytoscape-graph',
        elements=cyto_elements,
        style={'width': '100%', 'height': '600px'},
        layout={'name': 'cose'},  # automatic layout
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)',
                    'background-color': 'data(risk_color)',
                    'color': 'white',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'width': '250px',
                    'height': '80px',
                    'shape': 'round-rectangle',
                    'font-size': '12px'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'curve-style': 'bezier',
                    'target-arrow-shape': 'triangle',
                    'line-color': '#888',
                    'target-arrow-color': '#888',
                    'width': 3
                }
            }
        ]
    ),
    html.Div(id='node-info', style={'marginTop': '20px', 'fontSize': '16px'})
])

# ---------------------------
# Callback for tooltip / node info
# ---------------------------
@app.callback(
    Output('node-info', 'children'),
    Input('cytoscape-graph', 'tapNodeData')
)
def display_node_info(data):
    if data:
        risk = data.get('risk', 'Not defined')
        return f"Clause: {data['label']} | Risk: {risk}"
    return "Click a node to see details."

# ---------------------------
# Run server
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)
