from graphviz import Digraph

def create_workflow_graph():
    dot = Digraph(comment='FingerChain Workflow', format='png')
    dot.attr(rankdir='TB', size='8,10')

    # Nodes
    dot.node('start', 'Start', shape='oval')
    dot.node('deploy', 'Deploy Fabric Network\nand Chaincode', shape='box')
    dot.node('owner_reg', 'Owner Registers\n(owner1)', shape='box')
    dot.node('upload', 'Upload Media\nto IPFS', shape='box')
    dot.node('user_reg', 'User Registers\n(user1)', shape='box')
    dot.node('share', 'Share Media\nwith User', shape='box')
    dot.node('fingerprint', 'User Embeds\nFingerprint (b_k)', shape='box')
    dot.node('trace', 'Trace Fingerprint\nfor Piracy', shape='box')
    dot.node('end', 'End', shape='oval')

    # Edges
    dot.edges(['start->deploy', 'deploy->owner_reg', 'owner_reg->upload',
               'upload->user_reg', 'user_reg->share', 'share->fingerprint',
               'fingerprint->trace', 'trace->end'])

    # Save
    dot.render('workflow', cleanup=True)
    print('Flowchart saved as workflow.png')

if __name__ == '__main__':
    create_workflow_graph()