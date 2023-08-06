import os
import pandas as pd
from simio_lisa.utils import *


def check_results_dict_dimensions(result_dict: dict):
    """
    Check that all keys in results dictionary have the same dimension.
    :param result_dict: Results of dictionary.
    :return: Nothing.
    """
    check_list = []
    error_message = []
    for key, value in result_dict.items():
        error_message.append(f'{key}: {", ".join([str(item) for item in value])}\n')
        check_list.append(len(value))
    if len(set(check_list)) > 1:
        raise ValueError(f'Result dictionary has unbalanced values: {"; ".join(error_message)}')


def get_single_response_value(dom_response_list: list, agg_function):
    """
    Get value of a single scenario's response.
    :param dom_response_list: Single response provided as a list of one term.
    :param agg_function: Function to aggregate multiple responses.
    :return: Value of such observation.
    """
    response_list = extract_list_from_dom(dom_object=dom_response_list[0],
                                          tag_name='Observation',
                                          attribute_name='Value')
    if len(response_list) == 0:
        response_value = np.NaN
    else:
        try:
            response_value = agg_function([float(item) for item in response_list])
        except TypeError:
            response_value = np.NaN
    return response_value


def load_scenario_results(result_dict: dict,
                          dom_scenario_list: minidom.Document,
                          response_list: set,
                          scenario_name: str,
                          agg_function=np.mean):
    """
    Load scenario response and value to result_dict. Scenario name is set outside this function.
    :param scenario_name:
    :param result_dict: Dictionary of results to be updated.
    :param dom_scenario_list: List of.
    :param response_list: Set of response names to iterate over.
    :param agg_function: Aggregate responses.
    :return: Nothing. Result dictionary is updated
    """
    for resp in response_list:
        response = filter_dom_by_attribute(list_of_doms=dom_scenario_list,
                                           attribute_name='Response',
                                           attribute_value=resp)
        value_response = get_single_response_value(dom_response_list=response, agg_function=agg_function)
        result_dict['scenario'].append(scenario_name)
        result_dict['response'].append(resp)
        result_dict['value'].append(value_response)


def load_single_experiment_result(experiment_path: str, agg_function=np.mean) -> Union[pd.DataFrame, None]:
    """
    Load results of single experiment
    :param experiment_path:
    :param agg_function:
    :return: DataFrame with result of experiment.
    """
    try:
        project_xml = minidom.parse(experiment_path)
    except FileNotFoundError:
        warnings.warn(f'Experiment {experiment_path} has not been ran yet.')
        return None
    scenarios_names = set(extract_list_from_dom(dom_object=project_xml,
                                                tag_name='Observations',
                                                attribute_name='Scenario'))
    response_names = set(extract_list_from_dom(dom_object=project_xml,
                                               tag_name='Observations',
                                               attribute_name='Response'))
    results_dict = {'scenario': list(), 'response': list(), 'value': list()}
    for sce in scenarios_names:
        scenario_list = filter_dom_by_attribute(list_of_doms=extract_list_from_dom(dom_object=project_xml,
                                                                                   tag_name='Observations'),
                                                attribute_name='Scenario',
                                                attribute_value=sce)
        load_scenario_results(result_dict=results_dict,
                              dom_scenario_list=scenario_list,
                              response_list=response_names,
                              scenario_name=sce,
                              agg_function=agg_function)
        check_results_dict_dimensions(results_dict)
    results_df = pd.DataFrame(results_dict)
    results_df = results_df.pivot(index='scenario', columns='response', values='value')
    return results_df


def load_experiment_results(project_path: str,
                            project_filename: str,
                            model_name: str,
                            agg_function=np.mean) -> dict:
    """
    Load all experiment results related to a Simio model.
    :param project_path:
    :param project_filename:
    :param model_name:
    :param agg_function:
    :return: Dictionary whose keys are experiment name and value is a data frame (or None).
    """
    file_path = os.path.join(project_path, project_filename)
    experiment_list = get_experiment_names(path=file_path, model_name=model_name)
    folder_name = get_project_folder_name(project_file_name=project_filename)
    experiment_dictionary = {}
    for exp_name in experiment_list:
        experiments_path = os.path.join(project_path, folder_name, 'Results', model_name, exp_name)
        experiment_dictionary[exp_name] = load_single_experiment_result(experiment_path=experiments_path,
                                                                        agg_function=agg_function)
    return experiment_dictionary


def get_experiment_names(path: str,
                         model_name: str):
    """
    List of experiment names.
    :param path: path to Simio project.
    :param model_name: Name of the file.
    :return: List of experiment names.
    """
    project_xml = minidom.parse(path)
    list_of_models = extract_list_from_dom(dom_object=project_xml, tag_name='Model')
    model = get_model_from_list_of_doms(list_of_doms=list_of_models, model_name=model_name)
    experiment_list = extract_list_from_dom(dom_object=model,
                                            tag_name='Experiment',
                                            attribute_name='Name',
                                            suffix_str=' ResponseResults.xml')
    return experiment_list


def get_output_table_names(output_table_path: str):
    """
        List of output table names names.
        :param output_table_path: path to Simio project.
        :return: List of output table names.
    """

    all_table_names = os.listdir(output_table_path)
    output_table = [item for item in all_table_names if item.startswith('Output')]
    return output_table


def get_model_tables_path(project_path, model_name, project_filename):
    folder_name = get_project_folder_name(project_file_name=project_filename)
    return os.path.join(project_path, folder_name, 'Models', model_name, 'TableData')


def get_single_row_value(dom_row_list: list):
    """
    Get value of a single scenario's response.
    :param dom_row_list: Single row provided as a list of one term.
    :return: Value of such observation.
    """
    row_list = extract_list_from_dom(dom_object=dom_row_list,
                                     attribute_name='Value')
    if len(row_list) == 0:
        response_value = np.NaN
    else:
        response_value = row_list[0]
    return response_value


def add_row_to_table(result_dict: dict,
                     dom_row: minidom.Document,
                     column_names: set):
    """
    Load row to table
    :param result_dict: Dictionary of results to be updated.
    :param dom_row: List of.
    :param column_names: Set of response names to iterate over.
    :return: Nothing. Result dictionary is updated
    """
    row = dom_row.getElementsByTagName('StateValue')
    for resp in column_names:
        response = filter_dom_by_attribute(list_of_doms=row,
                                           attribute_name='Name',
                                           attribute_value=resp)
        value_response = get_single_row_value(dom_row_list=response)
        result_dict[resp].append(value_response)


def get_column_names(row_doms):
    column_names = list()
    for i in row_doms:
        column_names.extend(extract_list_from_dom(dom_object=i,
                                                  tag_name='StateValue',
                                                  attribute_name='Name'))
    column_names = set(column_names)
    return column_names


def load_single_output_table(table_path: str) -> Union[pd.DataFrame, None]:
    """
    Load results of single experiment
    :param table_path:
    :return: DataFrame with result of experiment.
    """
    try:
        project_xml = minidom.parse(table_path)
    except FileNotFoundError:
        warnings.warn(f'Table {table_path} has not been ran yet.')
        return None
    row_doms = extract_list_from_dom(dom_object=project_xml,
                                     tag_name='Row')
    if len(row_doms) == 0:
        warnings.warn(f'Table {table_path} is empty')
        return None
    column_names = get_column_names(row_doms=row_doms)
    results_dict = {col: [] for col in column_names}
    for row in row_doms:
        add_row_to_table(result_dict=results_dict,
                         dom_row=row,
                         column_names=column_names)
        check_results_dict_dimensions(results_dict)
    results_df = pd.DataFrame(results_dict)
    return results_df


def load_output_tables(project_path: str,
                       project_filename: str,
                       model_name: str):
    """
        Load all experiment results related to a Simio model.
        :param project_path:
        :param project_filename:
        :param model_name:
        :return: Dictionary whose keys are experiment name and value is a data frame (or None).
        """
    output_tables_path = get_model_tables_path(project_path=project_path,
                                               project_filename=project_filename,
                                               model_name=model_name)
    output_file_list = get_output_table_names(output_table_path=output_tables_path)
    experiment_dictionary = dict()
    for _table_name in output_file_list:
        table_path = os.path.join(output_tables_path, _table_name)
        experiment_dictionary[_table_name.split('.')[0]] = load_single_output_table(table_path)
    return experiment_dictionary


if __name__ == '__main__':
    env_project_path = os.environ['SIMIOPROJECTPATH']
    env_project_file = os.environ['SIMIOPROJECTNAME']
    env_model_name = os.environ['MODELNAME']
    # env_export_dir = os.environ['EXPORTDIR']
    # output_tables = load_output_tables(project_path=env_project_path,
    #                                   project_filename=env_project_file,
    #                                   model_name=env_model_name)
    # for table_name, table_df in output_tables.items():
    #    print(os.path.join(env_export_dir, f'{table_name}.csv'))
    #    table_df.to_csv(os.path.join(env_export_dir, f'{table_name}.csv'), index=False)
    experiments_df = load_experiment_results(project_path=env_project_path,
                                             project_filename=env_project_file,
                                             model_name=env_model_name,
                                             agg_function=np.mean)
