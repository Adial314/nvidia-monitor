from custom.Status import Status


if __name__ == "__main__":
    limits = {"temperature": 85}
    recipient = "seaborn.dev@gmail.com"
    status = Status("gpu_log.txt", "gpu_log.csv", limits=limits, recipient=recipient, debug=True)
    status.update()
