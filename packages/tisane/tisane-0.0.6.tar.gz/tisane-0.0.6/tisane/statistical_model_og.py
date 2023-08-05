from tisane.concept import Concept
from tisane.variable import (
    AbstractVariable,
    Nominal,
    Ordinal,
    Numeric,
    Has,
    Associates,
    Causes,
)
from tisane.random_effects import (
    RandomEffect,
    RandomSlope,
    RandomIntercept,
    CorrelatedRandomSlopeAndIntercept,
)
from tisane.effect_set import EffectSet, MainEffect, InteractionEffect, MixedEffect
from tisane.graph import Graph
from tisane.data import Dataset

from abc import abstractmethod
import pandas as pd
from typing import List, Any, Tuple
import typing
from itertools import chain, combinations
import json

##### HELPER #####
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


class StatisticalModel(object):
    # residuals: AbstractVariable
    # TODO: May not need properties since not sure what the properties would be if not the indivdiual variables or the residuals
    properties: list  # list of properties that this model exhibits

    fixed_ivs: List[AbstractVariable]
    interactions: List[Tuple[AbstractVariable, ...]]
    random_ivs: List[RandomEffect]
    family: str
    link_function: str  # maybe, not sure?
    variance_function: str  # maybe, not sure?

    graph: Graph  # IR

    consts: dict  # Z3 consts representing the model and its DV, fixed_ivs, etc.

    dataset: Dataset

    def __init__(
        self,
        dv: AbstractVariable = None,
        fixed_ivs: List[AbstractVariable] = None,
        interactions: List[Tuple[AbstractVariable, ...]] = None,
        random_ivs: List[RandomEffect] = None,
        family: str = None,
        link_func: str = None,
        dataset: Dataset = None,
    ):
        if dv:
            self.dv = dv

            self.graph = Graph()
            self.graph._add_variable(self.dv)

        if fixed_ivs is not None:
            self.set_fixed_ivs(fixed_ivs=fixed_ivs)
        else:
            self.fixed_ivs = list()

        # if random_slopes is not None:
        #     self.set_random_slopes(random_slopes=random_slopes)
        # else:
        #     self.random_slopes = list()

        # if random_intercepts is not None:
        #     self.set_random_intercepts(random_intercepts=random_intercepts)
        # else:
        #     self.random_intercepts = list()

        if random_ivs is not None:
            self.set_random_ivs(random_ivs=random_ivs)
        else:
            self.random_ivs = list()

        # Set interactions last in case Random Slope, Random Intercept adds identifier variables/relations we care about
        if interactions is not None:
            self.set_interactions(interactions=interactions)
        else:
            self.interactions = list()

        self.family = family
        self.link_function = link_func
        # self.variance_func = variance_func

        self.consts = dict()

        self.dataset = None

    # Associate this Study Design with a Dataset
    def assign_data(self, source: typing.Union[os.PathLike, pd.DataFrame]):
        self.dataset = Dataset(source)

        return self

    def __str__(self):
        dv = f"DV: {self.dv}\n"
        fixed_ivs = f"Main effects: {self.fixed_ivs}\n"
        interactions = f"Interaction effects: {self.interactions}\n"
        mixed_effects = f"Mixed effects: {self.mixed_effects}"

        return dv + fixed_ivs + interactions + mixed_effects

    # @return string of mathematical version of the statistical model
    # TODO: @param setting might tell us something about how to format the categorical variables...
    def mathematize(self, setting=None):
        def transform_var(var: AbstractVariable):
            if var.transform != "NoTransformation":
                return var.transform + "(" + var.name + ")"

            return var.name

        y = transform_var(self.dv)
        xs = list()

        for m in self.fixed_ivs:
            xs.append(transform_var(m))

        for i in self.interactions:
            x = "("
            # Iterate through variables involved in interaction
            for idx in range(len(i)):
                x += transform_var(i[idx])
                if idx + 1 < len(i):
                    x += "*"
            x += ")"
            xs.append(x)

        for mi in self.mixed_effects:
            # TODO: Implement, may want to do something special about slope vs. intercept vs. both....
            pass

        equation = y + " = " + "+".join(xs)
        return equation

    # Sets main effects to @param fixed_ivs
    def set_fixed_ivs(self, fixed_ivs: List[AbstractVariable]):
        self.fixed_ivs = fixed_ivs

        # Update the Graph IR
        for var in self.fixed_ivs:
            assert isinstance(var, AbstractVariable)
            conceptually_related = False
            for relationship in var.relationships:
                if isinstance(relationship, Cause):
                    cause = relationship.cause
                    effect = relationship.effect
                    if relationship.effect == self.dv:
                        self.graph.cause(cause, effect)
                        conceptually_related = True
                elif isinstance(relationship, Associate):
                    lhs = relationship.lhs
                    rhs = relationship.rhs
                    if relationship.lhs == self.dv or relationship.rhs == self.dv:
                        self.graph.associate(lhs, rhs)
                        conceptually_related = True
            if not conceptually_related:
                raise ValueError(
                    f"The independent variable {var.name} is not conceptually related to the dependent variable {self.dv.name}"
                )

    # Sets interaction effects to @param interactions, adding updates to the graph as needed
    def set_interactions(self, interactions: List[Tuple[AbstractVariable, ...]]):
        self.interactions = interactions

        for ixn in self.interactions:
            ixn_name = list()
            # TODO: interaction_data = DataVector()

            # Create ixn variable
            for variable in ixn:
                ixn_name.append(variable.name)
                self.graph.get_variable
            ixn_var = Nominal("*".join(ixn_name))
            # Ixn contributes to DV
            self.graph.associate(lhs=ixn_var, rhs=self.dv)

            # Ixn variable 'inherits' has/identifier edges from component variables/nodes
            pre_identifiers = list()
            for variable in ixn:
                predecessors = self.graph.get_predecessors(
                    var=variable
                )  # returns a dict keyiterator

                if predecessors is not None:
                    for p in predecessors:
                        p_var = self.graph.get_variable(name=p)
                        p_node, p_data = self.graph.get_node(variable=p_var)
                        if p_data["is_identifier"]:
                            pre_identifiers.append(p_var)
                        # Also equivalent, could update?:
                        # if self.graph.has_edge(start=p_var, end=variable, edge_type='has'):
                        #     pre_identifiers.append(p_var)

            for pi in pre_identifiers:
                has_obj = pi.has(ixn_var)
                self.graph.has(
                    identifier=pi, variable=ixn_var, has_obj=has_obj, repetitions=1
                )

    # Sets random ivs
    def set_random_ivs(self, random_ivs: List[RandomEffect]):
        self.random_ivs = random_ivs

        # Update the Graph IR
        for re in random_ivs:

            if isinstance(re, RandomIntercept):
                group = re.groups

                # Add the random intercept
                for relationship in group.relationships:
                    if isinstance(relationship, Has):
                        identifier = relationship.variable
                        measure = relationship.measure

                        if identifier == group:
                            self.graph.has(
                                identifier,
                                measure,
                                relationship,
                                relationship.repetitions,
                            )

            elif isinstance(re, RandomSlope):
                iv = re.iv
                group = re.groups

                for relationship in group.relationships:
                    if isinstance(relationship, Has):
                        identifier = relationship.variable
                        measure = relationship.measure

                        if identifier == group:
                            self.graph.has(
                                identifier,
                                measure,
                                relationship,
                                relationship.repetitions,
                            )

                for relationship in iv.relationships:
                    if isinstance(relationship, Cause):
                        cause = relationship.cause
                        effect = relationship.effect
                        if relationship.effect == self.dv:
                            self.graph.cause(cause, effect)
                    elif isinstance(relationship, Associate):
                        lhs = relationship.lhs
                        rhs = relationship.rhs
                        if relationship.lhs == self.dv or relationship.rhs == self.dv:
                            self.graph.associate(lhs, rhs)

    # Sets the family
    def set_family(self, family: str):
        self.family = family

    # Sets the link function
    def set_link_function(self, link_function: str):
        self.link_function = link_function

    # @return all variables (DV, IVs)
    def get_variables(self) -> List[AbstractVariable]:
        variables = [self.dv] + self.fixed_ivs

        for ixn in self.interactions:
            for i in ixn:
                # Check that we haven't already added the variable (as a main effect)
                if i not in variables:
                    variables.append(i)

        # TODO for mixed effects!
        for mi in self.mixed_effects:
            pass

        return variables

    # @return a list containing all the IVs
    def get_all_ivs(self):
        return self.fixed_ivs + self.interactions + self.mixed_effects

    def add_main_effect(self, new_main_effect: AbstractVariable, **kwargs):
        if "edge_type" in kwargs:
            edge_type = kwargs["edge_type"]
        else:
            edge_type = "unknown"

        updated_fixed_ivs = self.fixed_ivs + [new_main_effect]
        # TODO: Update when move to Graph IR -- add a treat Graph function?
        self.graph._add_edge(start=new_main_effect, end=self.dv, edge_type=edge_type)

    # @return Z3 consts for variables in model
    def generate_consts(self):
        # Declare data type
        Object = DeclareSort("Object")

        # Create and add Z3 consts for all main effects
        fixed_ivs = self.fixed_ivs

        main_seq = None
        if len(self.fixed_ivs) > 0:
            for me in fixed_ivs:
                # Have we created a sequence of IVs yet?
                # If not, create one
                if main_seq is None:
                    # set first Unit of sequence
                    main_seq = Unit(me.const)
                # We already created a sequence of IVs
                else:
                    # Concatenate
                    main_seq = Concat(Unit(me.const), main_seq)
        # There are no main effects
        else:
            main_seq = Empty(SeqSort(Object))

        self.consts["fixed_ivs"] = main_seq

        # Create and add Z3 consts for Interaction effects
        interactions_seq = None
        if len(self.interactions) > 0:
            for ixn in self.interactions:
                tmp = EmptySet(Object)

                # For each variable in the interaction tuple
                for v in ixn:
                    tmp = SetAdd(tmp, v.const)

                # Do we already have a sequence we're building onto?
                # If not, create one
                assert tmp is not None
                if interactions_seq is None:
                    # Create a sequence
                    interactions_seq = Unit(tmp)
                # We already have a sequence of interactions
                else:
                    # Concatenate
                    interactions_seq = Concat(Unit(tmp), interactions_seq)
        # There are no interaction effects
        else:
            interactions_seq = Unit(EmptySet(Object))

        self.consts["interactions"] = interactions_seq

    # @returns the set of logical facts that this StatisticalModel "embodies"
    def compile_to_facts(self) -> List:
        facts = list()

        # Declare data type
        Object = DeclareSort("Object")

        # Add interaction effects
        if self.interactions is not None:
            # i_set is a Tuple of AbstractVariables
            for i_set in self.interactions:
                # Create set object
                tmp = EmptySet(Object)
                # Add each variable in the interaction set
                for v in i_set:
                    tmp = SetAdd(tmp, v.const)

                facts.append(Interaction(tmp))

        # Add link function
        if self.link_function is not None:
            if self.link_function == "Log":
                facts.append(LogTransform(self.dv.const))
            elif self.link_function == "Squareroot":
                facts.append(SquarerootTransform(self.dv.const))
            elif self.link_function == "LogLog":
                facts.append(LogLogTransform(self.dv.const))
            elif self.link_function == "Probit":
                facts.append(ProbitTransform(self.dv.const))
            elif self.link_function == "Logit":
                facts.append(LogitTransform(self.dv.const))
            else:
                raise ValueError(f"Link function not supproted: {self.link_function}")

        # Add variance function
        if self.variance_func is not None:
            if self.variance_func == "Gaussian":
                facts.append(Gaussian(self.dv.const))
            elif self.variance_func == "InverseGaussian":
                facts.append(InverseGaussian(self.dv.const))
            elif self.variance_func == "Binomial":
                facts.append(Binomial(self.dv.const))
            elif self.variance_func == "Multinomial":
                facts.append(Multinomial(self.dv.const))
            else:
                raise ValueError(
                    f"Variance function not supported: {self.variance_func}"
                )

        # Add variable data types
        variables = self.get_variables()
        for v in variables:
            if isinstance(v, Nominal):
                facts.append(NominalDataType(v.const))
            elif isinstance(v, Ordinal):
                facts.append(OrdinalDataType(v.const))
            elif isinstance(v, Numeric):
                facts.append(NumericDataType(v.const))
            elif isinstance(v, AbstractVariable):
                pass
            else:
                raise ValueError

        # Add structure facts
        edges = self.graph.get_nodes()
        for (n0, n1, edge_data) in edges:
            edge_type = edge_data["edge_type"]
            n0_var = gr.get_variable(n0)
            n1_var = gr.get_variable(n1)

            if edge_type == "treat":
                pass
                # # n0_var is unit
                # facts.append()
                # # n1_var is treatment
                # facts.append()

            elif edge_type == "nest":
                pass
                # TODO: Useful for mixed effects
            else:
                pass

            # What is the unit
            # What is the nesting

        return facts

    # @return additional set of logical facts that needs disambiguation depending on @param desired output_obj
    # def collect_ambiguous_facts(self, output: str) -> List:
    #     facts = list()
    #     edges = self.graph.get_edges() # get list of edges

    #     if output.upper() == 'VARIABLE RELATIONSHIP GRAPH':
    #         # Iterate over all edges
    #         # This covers all the interactions, too.
    #         for (n0, n1, edge_data) in edges:
    #             edge_type = edge_data['edge_type']
    #             n0_var = gr.get_variable(n0)
    #             n1_var = gr.get_variable(n1)
    #             if edge_type == 'unknown':
    #                 if output.upper() == 'VARIABLE RELATIONSHIP GRAPH':
    #                     # Induce UNSAT in order to get end-user clarification
    #                     facts.append(Cause(n0_var.const, n1_var.const))
    #                     facts.append(Correlate(n0_var.const, n1_var.const))
    #             else:
    #                 raise NotImplementedError
    #     elif output.upper() == 'STUDY DESIGN':
    #         # Data schema
    #         nodes = self.graph.get_nodes()
    #         for (n, data)  in nodes:
    #             n_var = data['variable']
    #             facts.append(NumericDataType(n_var.const))
    #             facts.append(CategoricalDataType(n_var.const))
    #             # TODO: Start here: Find data type info during prep_query?
    #             # Doing so seems to defeat purpose of interactive synth procedure...
    #             # Maybe I don't need to add these ambiguous facts since I have a link and variance functions?
    #             # Think through (1) have link and variance functions, (2) do not have (this seems like a separate pre-step...?)
    #             # Map out diagrammatically what looking for, etc.

    #             # facts.append(NominalDataType(n_var.const))
    #             # facts.append(OrdinalDataType(n_var.const))

    #         # Data collection procedure
    #         for (n0, n1, edge_data) in edges:
    #             edge_type = edge_data['edge_type']
    #             n0_var = gr.get_variable(n0)
    #             n1_var = gr.get_variable(n1)
    #             if edge_type == 'treat':
    #                 facts.append(Between(n1_var.const, n0_var.const))
    #                 facts.append(Within(n1_var.const, n0_var.const))

    #     return facts

    def query(self, outcome: str) -> Any:
        # Ground some rules to make the quantification simpler
        dv_const = self.consts["dv"]
        fixed_ivs = self.consts["fixed_ivs"]
        interactions = self.consts["interactions"]
        KB.ground_rules(
            dv_const=dv_const, fixed_ivs=fixed_ivs, interactions=interactions
        )

        # Collect facts based on @param outcome
        facts = self.collect_facts(outcome=outcome)
        # Collect rules based on @param outcome
        result = QM.query(outcome=outcome, facts=facts)

        if outcome.upper() == "VARIABLE RELATIONSHIP GRAPH":
            graph = Graph()
            # TODO: update graph based on result (Z3 model)
            return graph

    # def collect_facts(self, outcome: str):
    #     desired_outcome = outcome.upper()

    #     facts = list()
    #     if desired_outcome == 'STATISTICAL MODEL':
    #         raise NotImplementedError
    #     elif desired_outcome == 'VARIABLE RELATIONSHIP GRAPH':
    #         all_vars = self.consts['variables']
    #         dv_const = self.consts['dv']
    #         fixed_ivs = self.consts['fixed_ivs']
    #         interactions = self.consts['interactions']

    #         for v in all_vars:
    #             # Is the variable a main effect?
    #             if is_true(BoolVal(Contains(fixed_ivs, Unit(v)))):
    #                 if v is not dv_const:
    #                     facts.append(Cause(v, dv_const))
    #                     facts.append(Correlate(v, dv_const))
    #                 # Is the variable involved in an interaction?
    #                 # for i in interactions:
    #                 #     if is_true(BoolVal(IsMember(v, i))):

    #         if self.interactions:
    #             # TODO: Generalize this to more than 2 vars involved in an interaction
    #             for v0, v1 in self.interactions:
    #                 v0_const = None
    #                 v1_const = None
    #                 for v in all_vars:
    #                     if v0.name == str(v):
    #                         v0_const = v
    #                     if v1.name == str(v):
    #                         v1_const = v
    #                 # if v0_const and v1_const:
    #                 #     assert(is_true(BoolVal(IsMember(v0, ))))

    #                 # Have found both variables involved in the interaction
    #                 assert(v0_const is not None)
    #                 assert(v1_const is not None)
    #                 facts.append(Cause(v0_const, v1_const))
    #                 facts.append(Correlate(v0_const, v1_const))

    #     elif desired_outcome == 'DATA SCHEMA':
    #         pass
    #     elif desired_outcome == 'DATA COLLECTION PROCEDURE':
    #         raise NotImplementedError
    #     else:
    #         raise ValueError(f"Query is not supported: {outcome}. Try the following: 'STATISTICAL MODEL', 'VARIABLE RELATIONSHIP GRAPH', 'DATA SCHEMA', 'DATA COLLECTION PROCEDURE'")

    #     #
    #     return facts

    # #TODO: @return a DataSet object with data schema info only
    # def query_data_schema(self):
    #     ivs = self.get_all_ivs()
    #     model_facts = self.to_logical_facts()
    #     KB.query_data_schema(facts=model_facts, ivs=ivs, dv=[self.dv])

    # @property
    # def residuals(self):
    #     raise NotImplementedError

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a StatisticalModel according to type
        """

        global supported_model_types

        if "model_type" in kwargs.keys():
            mtype = kwargs["model_type"].upper()
            effect_set = kwargs["effect_set"]
            assert isinstance(effect_set, EffectSet)

            if mtype == "LINEAR_REGRESSION":
                return LinearRegression(effect_set)
            elif mtype == "LOGISTIC_REGRESSION":
                return LogisticRegression(effect_set)
            else:
                raise ValueError(
                    f"Model type {mtype} not supported! Try {','.join(supported_model_types)} "
                )

        else:
            raise ValueError(
                f"Please specify a model type! Try {','.join(supported_model_types)} "
            )

    # TODO: May not need this (see note next to properties PIV)
    def assert_property(self, prop: str, val: Any) -> None:
        key = prop.upper()
        self.properties[key] = val


# if only main effects and numeric dv --> LinearRegression

# Should we have more tiered Model -> Regression -> LinearRegression?

# if main effects and interaction effects -> Regression
