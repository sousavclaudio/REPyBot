import time
from enum import Enum


class ProcessState(Enum):
    INIT = "Init"
    GET_TRANSACTION_DATA = "GetTransactionData"
    PROCESS_TRANSACTION = "ProcessTransaction"
    END_PROCESS = "EndProcess"


class BusinessException(Exception):
    """Expected exception related to business rules."""
    pass


class SystemException(Exception):
    """Unexpected exception related to system/runtime issues."""
    pass


class SampleProcess:
    def __init__(self) -> None:
        self.transactions = []
        self.current_transaction = None
        self.transaction_index = 0
        self.processed_count = 0
        self.failed_count = 0
        self.state = ProcessState.INIT

    def run(self) -> None:
        print("Starting REPyBot sample process...\n")

        while self.state != ProcessState.END_PROCESS:
            try:
                if self.state == ProcessState.INIT:
                    self.init_process()

                elif self.state == ProcessState.GET_TRANSACTION_DATA:
                    self.get_transaction_data()

                elif self.state == ProcessState.PROCESS_TRANSACTION:
                    self.process_transaction()

            except BusinessException as exc:
                self.failed_count += 1
                print(f"[BUSINESS EXCEPTION] {exc}")
                self.state = ProcessState.GET_TRANSACTION_DATA

            except SystemException as exc:
                self.failed_count += 1
                print(f"[SYSTEM EXCEPTION] {exc}")
                print("Stopping process due to system exception.")
                self.state = ProcessState.END_PROCESS

            except Exception as exc:
                self.failed_count += 1
                print(f"[UNEXPECTED ERROR] {exc}")
                print("Stopping process due to unexpected error.")
                self.state = ProcessState.END_PROCESS

        self.end_process()

    def init_process(self) -> None:
        print("[INIT] Loading configuration and preparing environment...")

        # Simulated input transactions
        self.transactions = [
            {"id": 1, "name": "Transaction A", "status": "ok"},
            {"id": 2, "name": "Transaction B", "status": "business_error"},
            {"id": 3, "name": "Transaction C", "status": "ok"},
            {"id": 4, "name": "Transaction D", "status": "system_error"},
        ]

        time.sleep(1)
        print(f"[INIT] Loaded {len(self.transactions)} transactions.\n")
        self.state = ProcessState.GET_TRANSACTION_DATA

    def get_transaction_data(self) -> None:
        print("[GET TRANSACTION DATA] Retrieving next transaction...")

        if self.transaction_index >= len(self.transactions):
            print("[GET TRANSACTION DATA] No more transactions.\n")
            self.state = ProcessState.END_PROCESS
            return

        self.current_transaction = self.transactions[self.transaction_index]
        self.transaction_index += 1

        print(
            f"[GET TRANSACTION DATA] Current transaction: "
            f"{self.current_transaction['id']} - {self.current_transaction['name']}\n"
        )

        self.state = ProcessState.PROCESS_TRANSACTION

    def process_transaction(self) -> None:
        if not self.current_transaction:
            raise SystemException("No transaction loaded for processing.")

        print(
            f"[PROCESS TRANSACTION] Processing transaction "
            f"{self.current_transaction['id']}..."
        )

        status = self.current_transaction["status"]
        time.sleep(1)

        if status == "business_error":
            raise BusinessException(
                f"Business rule failed for transaction {self.current_transaction['id']}."
            )

        if status == "system_error":
            raise SystemException(
                f"System failure while processing transaction {self.current_transaction['id']}."
            )

        self.processed_count += 1
        print(
            f"[PROCESS TRANSACTION] Transaction "
            f"{self.current_transaction['id']} processed successfully.\n"
        )

        self.state = ProcessState.GET_TRANSACTION_DATA

    def end_process(self) -> None:
        print("[END PROCESS] Finalizing execution...")
        print(f"[END PROCESS] Processed successfully: {self.processed_count}")
        print(f"[END PROCESS] Failed: {self.failed_count}")
        print("[END PROCESS] REPyBot sample process finished.")


if __name__ == "__main__":
    process = SampleProcess()
    process.run()