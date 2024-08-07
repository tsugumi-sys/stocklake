class PrettyStdoutPrint:
    one_blank_space = " "
    two_blank_spaces = "  "
    msg_colors = {
        "FAIL": "\033[91m",
        "SUCCESS": "\033[92m",
        "WARNING": "\033[93m",
        "DEFAULT": "\033[0m",
    }

    def step_start(self, step_name: str):
        print(
            "{}{}{}{}".format(
                "=" * 30,
                f"{step_name}",
                "=" * 30,
                self.msg_colors.get("DEFAULT"),
            )
        )

    def normal_message(self, message: str):
        print(
            "{}{}{}".format(
                self.one_blank_space * 2,
                message,
                self.msg_colors.get("DEFAULT"),
            )
        )

    def success_message(self, message: str):
        print(
            "{}{}{}{}".format(
                self.msg_colors.get("SUCCESS"),
                self.two_blank_spaces,
                message,
                self.msg_colors.get("DEFAULT"),
            )
        )

    def warning_message(self, message: str):
        print(
            "{}{}{}{}".format(
                self.msg_colors.get("WARNING"),
                self.two_blank_spaces,
                message,
                self.msg_colors.get("DEFAULT"),
            )
        )


class PipelineStdOut:
    def __init__(self, enable_stdout: bool = True):
        self.enable_stdout = enable_stdout
        self.stdout = PrettyStdoutPrint()

    def starting(self, pipeline_name: str):
        if self.enable_stdout:
            self.stdout.step_start(f"Pipeline: {pipeline_name} is starting ...")

    def skip_downloading(self):
        if self.enable_stdout:
            self.stdout.warning_message("- Skip Downloading")

    def downloading(self):
        if self.enable_stdout:
            self.stdout.normal_message("- Downloading ...")

    def completed(self, stored_location: str):
        if self.enable_stdout:
            self.stdout.success_message(
                f"- Completed🐳. The data is stored into {stored_location}"
            )
