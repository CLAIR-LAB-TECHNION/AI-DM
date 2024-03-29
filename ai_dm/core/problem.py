__author__ = 'sarah'

from abc import ABC, abstractmethod
import ai_dm.search.utils as utils


class Problem (ABC):

    """Problem superclass
       supporting COMPLETE
    """

    def __init__(self, initial_state, constraints, stochastic=False):

        # creating the initial state object
        self.current_state = utils.State(initial_state, False)
        self.constraints = constraints
        self.stochastic = stochastic



    # return the actions that are applicable in the current state
    @abstractmethod
    def get_applicable_actions_at_state(self, state):
        pass


    # return the actions that are applicable in the current state
    @abstractmethod
    def get_applicable_actions_at_node(self, node):
        pass

    # return the successors that will result from applying the action (without changing the state)
    @abstractmethod
    def get_successors(self, action, node):
        pass

    # return the action's cost
    @abstractmethod
    def get_action_cost(self, action, state):
        pass

    # does the state represent a goal state
    @abstractmethod
    def is_goal_state(self, state):
        pass

    @abstractmethod
    def apply_action(self, action):
        pass

    @abstractmethod
    def reset_env(self):
        pass


    # get the current state
    def get_current_state(self):
        return self.current_state


    # value of a node
    def evaluate(self, node, use_cost_as_value=True):
        if use_cost_as_value:
            return node.get_path_cost(self)[0]
        # use value
        else:
            return node.get_path_value(self)[0]

    # return whether val_a is better or equal to val_b in the domain
    def is_better_or_equal(self, val_a, val_b):
        if val_a > val_b or val_a == val_b:
            return True
        else:
            return False

    # is the state valid in the domain
    def is_valid(self, state):

        # if there are no constraints - return True
        if self.constraints is None:
            print('No constraints')
            return True
        # check all constraints - if one is violated, return False
        for constraint in self.constraints:
            if not constraint.is_valid(state):
                return False
        # non of the constraints have been violated
        return True

    # get all successors for cur_node
    def successors(self, cur_node):

        # get the actions that can be applied to this node
        action_list = self.get_applicable_actions_at_node(cur_node)
        if action_list is None:
            return None

        # remove the successors that violate the constraints
        successor_nodes = []
        for action in action_list:

            successor_nodes_cur_action = self.get_successors(action, cur_node)
            for successor_node in successor_nodes_cur_action:
                valid = True
                # iterate through the constraints to see if the current action or successor states violate them
                for constraint in self.constraints:
                    if not constraint.is_valid(successor_node, action):
                        valid = False
                        break

                # add the node to the successor list
                if valid:
                    successor_nodes.append(successor_node)

        return successor_nodes


# problems with a discrete set of actions, and a defined probability function
class ProblemP (Problem):

    def __init__(self, initial_state, constraints, stochastic=False, P_func=None):
        super().__init__(initial_state, constraints, stochastic)
        self.P_func = P_func

    # get the actions that can be applied at the current node
    def get_applicable_actions_at_node(self, node):
        action_list = self.P_func[node.state.get_key()].keys()
        return action_list

    # get the actions that can be applied at the current node
    def get_applicable_actions_at_state(self, state):
        action_list = self.P_func[state.get_key()].keys()
        return action_list


# problems with a continous set of actions, for which an actions sampling procedure is defined for a given state
class ProblemS (Problem):

    def __init__(self, initial_state, constraints, stochastic=False):
        super().__init__(initial_state, constraints, stochastic)


    # return the actions that are applicable in the current state
    @abstractmethod
    def sample_applicable_actions_at_state(self, state, sample_size):
            pass
