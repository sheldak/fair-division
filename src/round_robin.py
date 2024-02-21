def round_robin(agents, allocation, items, ordering, steps="inf"):
    step = 0
    while items.size() > 0 and (steps == "inf" or step < steps):
        agent = agents.get_agent(ordering[step % agents.size()])
        favorite_item = get_favorite_item(agent, items)
        
        allocation.allocate(agent, favorite_item)

        items.delete_item(favorite_item)

        step += 1

    return (allocation, items)


def get_favorite_item(agent, items):
    favorite_item = None
    
    for item in items:
        if favorite_item is None or agent.get_valuation(item) > agent.get_valuation(favorite_item):
            favorite_item = item

    return favorite_item