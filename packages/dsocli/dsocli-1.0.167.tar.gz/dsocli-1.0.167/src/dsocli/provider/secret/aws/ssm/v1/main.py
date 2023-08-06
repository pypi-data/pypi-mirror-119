import boto3
from dsocli.exceptions import DSOException
from dsocli.logger import Logger
from dsocli.config import Configs
from dsocli.providers import Providers
from dsocli.secrets import SecretProvider
from dsocli.stages import Stages
from dsocli.constants import *
from dsocli.dict_utils import set_dict_value
from dsocli.contexts import Contexts
from dsocli.aws_utils import *


_default_spec = {
    'prefix': '/dso/v1/secrets'
}

def get_default_spec():
    return _default_spec.copy()


class AwsSsmSecretProvider(SecretProvider):


    def __init__(self):
        super().__init__('secret/aws/ssm/v1')


    def get_prefix(self):
        return Configs.secret_spec('prefix')



    def list(self, project, application, stage, uninherited=False, decrypt=False, filter=None):
        secrets = load_context_ssm_parameters(project, application, stage, 'SecureString', prefix=self.get_prefix(), uninherited=uninherited, decrypt=decrypt, filter=filter)
        result = {'Secrets': []}
        for key, details in secrets.items():
            item = {
                'Key': key,
                'RevisionId': str(details['Version']),
            }
            item.update(details)
            result['Secrets'].append(item)

        return result



    def add(self, project, application, stage, key, value):
        Logger.debug(f"Checking SSM secret overwrites: project={project}, application={application}, stage={stage}, key={key}")
        assert_ssm_parameter_no_namespace_overwrites(project, application, stage, key, prefix=self.get_prefix())
        Logger.debug(f"Locating SSM secret: project={project}, application={application}, stage={stage}, key={key}")
        found = locate_ssm_parameter_in_context_hierachy(project, application, stage, key, prefix=self.get_prefix(), uninherited=True)
        if found and not found['Type'] == 'SecureString':
            raise DSOException(f"Failed to add secret '{key}' becasue becasue the key is not available in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        path = get_ssm_path(project, application, stage=stage, key=key, prefix=self.get_prefix())
        Logger.info(f"Adding SSM secret: path={path}")
        response = put_ssm_secret(path, value)
        result = {
                'RevisionId': str(response['Version']),
                'Key': key, 
                'Value': value,
                'Stage': Stages.shorten(stage),
                'Scope': Contexts.translate_context(project, application, stage),
                'Origin': {
                    'Project': project,
                    'Application': application,
                    'Stage': Stages.shorten(stage),
                },
            }
        result.update(response)
        return result




    def get(self, project, application, stage, key, decrypt=False, revision=None):
        Logger.debug(f"Locating SSM secret: project={project}, application={application}, stage={stage}, key={key}")
        found = locate_ssm_parameter_in_context_hierachy(project, application, stage, key, prefix=self.get_prefix())
        if not found:
            raise DSOException(f"Secret '{key}' not found nor inherited in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        else:
            if not found['Type'] == 'SecureString':
                raise DSOException(f"Parameter '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        Logger.info(f"Getting SSM secret: path={found['Name']}")
        response = get_ssm_secret_history(found['Name'], decrypt)
        secrets = sorted(response['Parameters'], key=lambda x: int(x['Version']), reverse=True)
        if revision is None:
            ### get the latest revision
            result = {
                    'RevisionId': str(secrets[0]['Version']),
                    'Date': secrets[0]['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                    'Key': key, 
                    'Value': secrets[0]['Value'],
                    'Scope': found['Scope'],
                    'Origin': found['Origin'],
                    'Path': found['Name'],
                    'User': secrets[0]['LastModifiedUser'],
                    }
        else:
            ### get specific revision
            secrets = [x for x in secrets if str(x['Version']) == revision]
            if not secrets:
                raise DSOException(f"Revision '{revision}' not found for secret '{key}' in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
            result = {
                    'RevisionId': str(secrets[0]['Version']),
                    'Date': secrets[0]['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                    'Key': key, 
                    'Value': secrets[0]['Value'],
                    'Scope': found['Scope'],
                    'Origin': found['Origin'],
                    'Path': found['Name'],
                    'User': secrets[0]['LastModifiedUser'],
                    }

        return result



    def history(self, project, application, stage, key, decrypt=False):
        found = locate_ssm_parameter_in_context_hierachy(project, application, stage, key, prefix=self.get_prefix())
        if not found:
            raise DSOException(f"Secret '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        else:
            if not found['Type'] == 'SecureString':
                raise DSOException(f"Parameter '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        Logger.info(f"Getting SSM secret: path={found['Name']}")
        response = get_ssm_secret_history(found['Name'], decrypt)
        secrets = sorted(response['Parameters'], key=lambda x: int(x['Version']), reverse=True)
        result = { "Revisions":
            [{
                'RevisionId': str(secret['Version']),
                'Date': secret['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                'Key': key,
                'Value': secret['Value'],
                # 'Scope': found['Scope'],
                # 'Origin': found['Origin'],
                'User': secret['LastModifiedUser'],
                # 'Path': found['Name'],
            } for secret in secrets]
        }

        return result



    def delete(self, project, application, stage, key):
        Logger.debug(f"Locating SSM secret: project={project}, application={application}, stage={stage}, key={key}")
        ### only secrets owned by the context can be deleted, hence uninherited=True
        found = locate_ssm_parameter_in_context_hierachy(project, application, stage, key, prefix=self.get_prefix(), uninherited=True)
        if not found:
                raise DSOException(f"Secret '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        else:
            # if len(found) > 1:
            #     Logger.warn(f"More than one secret found at '{found['Name']}'. The first one taken, and the rest were discarded.")
            if not found['Type'] == 'SecureString':
                raise DSOException(f"Secret '{key}' not found in the given context: project={project}, application={application}, stage={Stages.shorten(stage)}")
        Logger.info(f"Deleting SSM secret: path={found['Name']}")
        delete_ssm_parameter(found['Name'])
        return {
                'Key': key, 
                'Scope': found['Scope'],
                'Origin': found['Origin'],
                # 'Path': found['Name'],
                }



def register():
    Providers.register(AwsSsmSecretProvider())
