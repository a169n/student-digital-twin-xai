from src.common.settings import get_settings
from src.generator.synthetic import SyntheticDatasetGenerator


def main() -> None:
    """Entrypoint for local ML service tasks.

    TODO: Add CLI-style task selection (generate/features/train/infer/explain/validate).
    """

    settings = get_settings()
    generator = SyntheticDatasetGenerator()
    print(f"ML service environment: {settings.ml_env}")
    print(generator.describe())


if __name__ == "__main__":
    main()
