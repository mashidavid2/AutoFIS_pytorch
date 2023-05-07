import os
import sys
import argparse
import json
import yaml
import os.path as path
#module_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
module_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
# print(module_path)
if module_path not in sys.path:
    sys.path.append(module_path)
#sys.path.append(os.path.abspath(__file__))
from classes import ColumnInfo, ModelInfoMapper, RecommendationInfo
from executor import ExecutorFactory
from preprocess import TableReader
from utils import from_dict, yaml_to_model_dict, yaml_to_config_dict

package_path = path.dirname(path.dirname(path.abspath(__file__)))
config_path = path.join(package_path,'config')

def train():
    #for local use
    model_name = ''
    with open(path.join(config_path,'autofis_model_config.yaml'),'r') as f:
        model_yaml = yaml.safe_load(f)
    model_name, model_info_dict = yaml_to_model_dict(model_yaml)
    # with open(path.join(config_path,'data_config.yaml'),'r') as f:
    #     column_yaml = yaml.safe_load(f)
    # column_dict = yaml_to_config_dict(column_yaml)
    column_dict = {
        'rating_column': {'name': 'Rating', 'type': 'Numerical'},
        'user_id_column': {'name': 'UserID', 'type': 'Categorical'},
        'user_feature_columns': [
            {'name': 'Gender', 'type': 'Categorical'},
            {'name': 'Age', 'type': 'Categorical'},
            {'name': 'Occupation', 'type': 'Categorical'}
        ],
        'item_id_column': {'name': 'MovieID', 'type': 'Categorical'},
        'item_feature_columns': [
            {'name': 'Genres', 'type': 'Categorical'},
            {'name': 'Year', 'type': 'Numerical'}
        ],
        'timestamp_column': {'name': '', 'type': 'TimeStamp'}
    }
    current_path = path.dirname(path.abspath(__file__))
    save_dir = path.join(current_path, 'save')
    train_dir = path.join(current_path, 'tmp/dataset_ml-1m')
    interaction_path = path.join(train_dir, 'ml_1m_interaction_table.csv')
    user_path = path.join(train_dir, 'ml_1m_user_table.csv')
    item_path = path.join(train_dir, 'ml_1m_item_table.csv')
    model_info_mapper = ModelInfoMapper(model_name, model_info_dict)

    executor = ExecutorFactory.from_model_name(model_name)

    evaluation = executor.execute_train(
        models_info=model_info_mapper.model_infos,
        column_info=from_dict(ColumnInfo, column_dict),
        base_dir=train_dir,
        interaction_file_path=interaction_path,
        user_file_path=user_path,
        item_file_path=item_path,
        save_dir=save_dir,
    )

def parse_train_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--column_info', type=str, default='')
    parser.add_argument('--recommendation_info', type=str, default='')
    parser.add_argument('--models_info', type=str, default='') # 기존 version front 호환을 위한 임시 argument
    parser.add_argument('--top_k', type=int, default=10)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_train_args()
    # # column_info = {
    # #     'col_rating_name': {'name': 'Rating', 'type': 'num'},
    # #     'col_user_name': {'name': 'UserID', 'type': 'cat'},
    # #     'col_user_features': [
    # #         {'name': 'Gender', 'type': 'cat'},
    # #         {'name': 'Age', 'type': 'num'},
    # #         {'name': 'Occupation', 'type': 'cat'}
    # #     ],
    # #     'col_item_name': {'name': 'MovieID', 'type': 'cat'},
    # #     'col_item_features': [
    # #         # {'name': 'Genre', 'type': 'cat'},
    # #         {'name': 'Year', 'type': 'num'}
    # #     ],
    # #     'col_temporal_name': {'name': '', 'type': 'tem'}
    # # }
    # recommendation_info_cat_boost = {
    #     'recommendation_type': 'USER2ITEM',
    #     'model_name': 'CatBoost',
    #     'models_info': {
    #         'CatBoost': {
    #             'model_name': 'CatBoost',
    #             'epoch': 1000,
    #             'batch_size': 2048,
    #             'num_negative': 4,
    #             'learning_rate': 0.01,
    #             'depth': 10
    #             # 'depth': 1
    #         },
    #     }
    # }
    #
    # recommendation_info_autofis = {
    #     'recommendation_type': 'USER2ITEM',
    #     'model_name': 'AutoFis',
    #     'models_info': {
    #         'AutoFis': {
    #             'model_name': 'AutoFis',
    #             'batch_size': 2048,
    #             'num_negative': 4,
    #             'learning_rate': 0.001,
    #             'latent_dim': 10,
    #             'epoch': 100,
    #         },
    #     }
    # }
    # # args.column_info = json.dumps(column_info)
    # args.recommendation_info = json.dumps(recommendation_info_autofis)
    # # args.recommendation_info = json.dumps(recommendation_info_cat_boost)
    train()
