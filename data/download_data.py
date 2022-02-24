""" Module with script to download public data
"""
import os
import sys
from pathlib import Path

import requests
import tqdm


FILES_TO_DOWNLOAD = [
    {
        "filename": "chembl_10k_route_distance_model.ckpt",
        "url": "https://zenodo.org/record/4925903/files/chembl_10k_route_distance_model.ckpt?download=1",
    },
    {"filename": "n1-routes.json", "url": ""},
    {"filename": "n1-targets.txt", "url": ""},
    {"filename": "n1-stock.txt", "url": ""},
    {"filename": "n5-routes.json", "url": ""},
    {"filename": "n5-targets.txt", "url": ""},
    {"filename": "n5-stock.txt", "url": ""},
    {"filename": "uspto_raw_template_library.csv"},
    {"filename": "uspto_rxn_n1_raw_template_library.csv"},
    {"filename": "uspto_rxn_n5_raw_template_library.csv", "url": ""},
    {"filename": "uspto_rxn_n1_keras_model.hdf5", "url": ""},
    {"filename": "uspto_rxn_n1_unique_templates.hdf5", "url": ""},
    {"filename": "uspto_rxn_n5_keras_model.hdf5"},
    {"filename": "uspto_rxn_n5_unique_templates.hdf5"},
    {"filename": "150k_routes.json.gz"},
]


def _download_file(url: str, filename: str) -> None:
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        pbar = tqdm.tqdm(
            total=total_size, desc=os.path.basename(filename), unit="B", unit_scale=True
        )
        with open(filename, "wb") as fileobj:
            for chunk in response.iter_content(chunk_size=1024):
                fileobj.write(chunk)
                pbar.update(len(chunk))
        pbar.close()


def main() -> None:
    """Entry-point for CLI"""
    base_path = Path(__file__).parent
    for filespec in FILES_TO_DOWNLOAD:
        try:
            _download_file(
                filespec["url"], os.path.join(base_path, filespec["filename"])
            )
        except requests.HTTPError as err:
            print(f"Download failed with message {str(err)}")
            sys.exit(1)


if __name__ == "__main__":
    main()