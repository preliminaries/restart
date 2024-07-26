"""Module setup.py"""
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.bucket


class Setup:
    """
    Description
    -----------

    Sets up local & cloud environments
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters

    def __s3(self, bucket_name: str) -> bool:
        """
        Prepares an Amazon S3 (Simple Storage Service) bucket.

        :param bucket_name:
        :return:
        """

        # An instance for interacting with Amazon S3 buckets.
        bucket = src.s3.bucket.Bucket(service=self.__service, location_constraint=self.__s3_parameters.location_constraint,
                                      bucket_name=bucket_name)

        if bucket.exists():
            return bucket.empty()

        return bucket.create()

    def exc(self) -> bool:
        """

        :return:
        """

        for bucket_name in [self.__s3_parameters.internal, self.__s3_parameters.external]:
            try:
                self.__s3(bucket_name=bucket_name)
            except RuntimeError as err:
                raise err from err

        return True
