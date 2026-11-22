# Mini project 2026

## Group rules
See our [group rules](grouprules.md)

## Product backlog

[Product backlog](https://github.com/users/BoddyGus/projects/4)

## Sprint 1 backlog

[Sprint 1 backlog](https://github.com/users/BoddyGus/projects/4/views/3)

## Sprint 2 backlog  

[Sprint 2 backlog](https://github.com/users/BoddyGus/projects/4/views/4)   

## DoD

A task is complete when:

- the functionality has been implemented
- all tests pass
- GitHub Actions completes successfully
- the change has been reviewed
- the pull request has been merged into the `main` branch

## OKD
Link to the application:
https://route-ohjelmistotuotanto-lahiopetus-2026-18.ext.okd-cs-test-0.k8s.cs.helsinki.fi

## Local setup

Create a `.env` file in the project root:
```env
DATABASE_URL=sqlite:///test.db
SECRET_KEY=dev-secret
TEST_ENV=true
```

Then run:
```bash
cd Ohjelmistotuotanto2026
uv sync
uv run python src/db_helper.py
uv run python src/index.py
```

Finally open: http://localhost:5001
