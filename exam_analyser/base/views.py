from copy import deepcopy

from rest_framework.exceptions import NotAcceptable

from exam_analyser.base.helpers import is_int


class CheckParamsMixin:
    """
    Mixin to check if query parameters or kwargs parameters are present, with the valid options.
    The `query_params_dict` can be set on view directly or can be set on constructor initialization, if dynamic
    options are to be loaded.
    """

    query_params_dict = {}  # example: {"query_name": []}

    def check_params(self, request, *args, **kwargs):
        """Check if the query parameter is passed with proper options."""

        # add kwargs params and query params
        params_dict = self.get_all_params(request, **kwargs)

        for query_param, options in self.query_params_dict.items():
            option = params_dict.get(query_param, None)
            breakpoint()
            if not option:
                raise NotAcceptable(
                    detail=f"This parameter is required: {query_param}."
                )
            if not self.is_valid_option_passed(
                passed_option=option, allowed_options=options
            ):
                raise NotAcceptable(
                    detail=f"Invalid option passed for: {query_param}. "
                    f"Allowed options are: {', '.join(str(_) for _ in options)}"
                )

        return None

    @staticmethod
    def is_valid_option_passed(passed_option, allowed_options):
        """
        The params passed in the urls are taken as a string, while the `allowed_options` can either be a
        list of string or integers, so this method irrespective of the type, checks if the option is valid.
        """

        if allowed_options is None:
            # if query_params_dict = {"input": None} | any input from user is accepted
            return True

        if (str(passed_option) in allowed_options) or (
            is_int(passed_option) and int(passed_option) in allowed_options
        ):
            return True

        # if any class is passed
        if len(allowed_options) >= 1 and allowed_options[0].__class__.__name__ in [
            "UUID"
        ]:
            allowed_options = [str(_) for _ in allowed_options]
            if passed_option in allowed_options:
                return True

        return False

    @staticmethod
    def get_all_params(request, **kwargs):
        """Returns all the parameters that are pass to the request. Includes parameters and url variables."""

        params_dict = deepcopy(request.query_params)
        params_dict.update(kwargs)
        return params_dict
