"""The Java Platform diagrams. Each function draws one diagram on a Canvas."""
from kit import Canvas

W = 1500


def overview(theme):
    c = Canvas(theme, W, 1176, "Java Platform: four repositories, layered from account foundation to application.")
    # infra-bootstrap
    c.band(24, 24, 1452, 260, "blue", "infra-bootstrap", "Account foundation · applied once by an administrator")
    cards = [("bucket", "storage", "Terraform state", "S3 + native locking"),
             ("bucket", "storage", "Release artifacts", "versioned app.jar"),
             ("git", "github", "GitHub OIDC", "no stored AWS keys"),
             ("shield", "security", "Guardrails", "permissions boundary"),
             ("trail", "mgmt", "CloudTrail", "account audit log"),
             ("r53", "network", "Hosted zone", "imported, protected")]
    for i, (g, cat, ti, sub) in enumerate(cards):
        c.card(48 + (i % 3) * 242, 112 + (i // 3) * 78, 228, g, cat, ti, sub)
    c.panel(784, 104, 668, 158, title="Deployment roles (+ a read-only plan twin each)")
    for i, (a, b) in enumerate([("platform", "dev"), ("platform", "prod"), ("platform", "shared"),
                                ("ami", None), ("workload", "dev"), ("workload", "prod")]):
        c.role(798 + i * 108, 146, 100, a, b)
    c.arrow([(750, 284), (750, 318)], "blue", "roles · buckets · zone", 764, 306, anchor="start")

    # platform-infra
    c.band(24, 320, 1452, 360, "green", "platform-infra", "Networks, keys and certificates · no application resources")
    c.card(1206, 338, 246, "cloud", "network", "Build VPC", "isolated, for Image Builder")
    c.panel(48, 408, 1404, 252, title="VPC per environment · dev 10.10.0.0/16 · prod 10.20.0.0/16", glyph="cloud", cat="network")
    groups = [(64, "green", "Public subnets", [("eu-west-1a", "ALB only"), ("eu-west-1b", "ALB only")]),
              (526, "blue", "Private app subnets", [("eu-west-1a", "EC2, EFS, endpoints"), ("eu-west-1b", "EC2, EFS")]),
              (988, "purple", "Private database subnets", [("eu-west-1a", "RDS primary"), ("eu-west-1b", "standby in prod")])]
    for x, tone, title, items in groups:
        c.panel(x, 452, 448, 104, tone, title, dashed=True, title_center=True)
        for j, (a, b) in enumerate(items):
            c.small(x + 16 + j * 216, 494, 200, "lock", "network", a, b, tone)
    row = [("arch", "network", "Internet gateway", "public subnets only"),
           ("list", "network", "Route tables", "no internet in private"),
           ("shield", "security", "Security groups", "SG-to-SG rules"),
           ("endpoint", "network", "VPC endpoints", "SSM, secrets, logs, S3"),
           ("key", "security", "KMS key", "one per environment"),
           ("cert", "security", "ACM certificate", "DNS-validated TLS")]
    for i, (g, cat, ti, sub) in enumerate(row):
        c.card(64 + i * 229, 576, 216, g, cat, ti, sub)
    c.arrow([(750, 680), (750, 714)], "green", "VPC, subnets, key, cert → SSM", 764, 702, anchor="start")

    # java-ami
    c.band(24, 716, 1452, 150, "orange", "java-ami", "App AMI · EC2 Image Builder")
    c.panel(360, 736, 1092, 110)
    steps = [("layers", "compute", "AL2023 arm64", "patched at build time"),
             ("gear", "compute", "Install runtime", "Corretto 21 + agents"),
             ("doc", "compute", "Bake release", "app.jar + services"),
             ("ami", "compute", "Tested app AMI", "exact ID, no latest")]
    for i, (g, cat, ti, sub) in enumerate(steps):
        x = 376 + i * 277
        c.card(x, 759, 229, g, cat, ti, sub, boxed=False)
        if i < 3:
            c.arrow([(x + 232, 791), (x + 270, 791)], "orange")
    c.arrow([(750, 866), (750, 900)], "orange", "exact AMI ID → dev, then promoted to prod", 764, 888, anchor="start")

    # java-infra
    c.band(24, 902, 1452, 250, "purple", "java-infra (application)", "Runs the Java service on the platform")
    c.card(48, 991, 240, "r53", "network", "Route 53", "dev.margarita.c-loud.am", boxed=False)
    c.arrow([(290, 1023), (316, 1023)], "purple")
    c.card(320, 991, 250, "alb", "network", "Load balancer", "HTTPS · WAF in prod", boxed=False)
    c.arrow([(572, 1023), (598, 1023)], "purple")
    c.panel(600, 968, 360, 104, "blue", "Java application tier", dashed=True, title_center=True)
    c.card(612, 1000, 336, "asg", "compute", "Auto Scaling group", "app AMI · private subnets", boxed=False)
    c.arrow([(960, 1023), (998, 1023)], "purple")
    c.panel(1000, 968, 452, 104, "purple", "Data tier", dashed=True, title_center=True)
    c.card(1012, 1000, 214, "db", "database", "RDS MySQL 8.4", "Multi-AZ in prod", boxed=False)
    c.card(1232, 1000, 214, "folder", "storage", "EFS", "shared files, TLS", boxed=False)
    for i, (g, cat, ti, sub) in enumerate([("watch", "mgmt", "CloudWatch", "logs, metrics, alarms"),
                                           ("vault", "security", "Secrets Manager", "DB password, rotated"),
                                           ("gear", "mgmt", "Settings from SSM", "no user data"),
                                           ("mail", "mgmt", "SNS", "alarm email")]):
        c.card(320 + i * 285, 1080, 270, g, cat, ti, sub, boxed=False)
    return c.render()


def identity(theme):
    c = Canvas(theme, W, 520, "How a pipeline gets AWS access through GitHub OIDC, and the GitHub controls managed as code.")
    c.band(24, 24, 1452, 250, "gray", "How a pipeline gets AWS access",
           "No AWS keys in GitHub: every job exchanges a short-lived OIDC token for its own role")
    flow = [("play", "github", "GitHub Actions job", "declares an environment"),
            ("token", "neutral", "OIDC token", "repo + env by immutable ID"),
            ("sts", "security", "AWS STS", "exact-match trust policy"),
            ("helmet", "security", "Deployment role", "1-hour credentials"),
            ("lock", "security", "Permissions boundary", "on roles it creates")]
    for i, (g, cat, ti, sub) in enumerate(flow):
        x = 48 + i * 277
        c.card(x, 112, 244, g, cat, ti, sub)
        if i < 4:
            c.arrow([(x + 247, 144), (x + 274, 144)], "gray")
    c.text(48, 226, "Every role carries", 14, muted=False, weight="600")
    for i, (g, ti, sub) in enumerate([("list", "ReadOnlyAccess", "reads everything"),
                                      ("bucket", "terraform-state", "its own state key"),
                                      ("shield", "github-actions-deploy-<repo>", "scoped writes"),
                                      ("check", "*-plan twin", "read-only, used by PRs")]):
        c.small(230 + i * 306, 198, 290, g, "security", ti, sub, "gray")
    c.band(24, 300, 1452, 196, "blue", "GitHub delivery controls", "Managed as code in infra-bootstrap (github.tf)")
    for i, (g, ti, sub) in enumerate([("branch", "Branch protection", "PR + green ci on main"),
                                      ("approve", "Production approval", "named reviewer"),
                                      ("lock", "Deploy from main only", "protected-branch policy"),
                                      ("var", "Variables & secrets", "role ARNs, switches, alert email")]):
        c.card(48 + i * 352, 392, 326, g, "github", ti, sub)
    return c.render()


def network(theme):
    c = Canvas(theme, W, 800, "Network: three tiers across two Availability Zones, AWS services reached privately, isolated build VPC.")
    c.band(24, 24, 1452, 752, "green", "platform-infra · network",
           "Two Availability Zones, three tiers, no internet route from private subnets")
    c.card(48, 104, 200, "user", "neutral", "Users", "HTTPS only")
    c.arrow([(250, 136), (288, 136)], "green")
    c.card(290, 104, 220, "r53", "network", "Route 53", "alias to the ALB")
    c.arrow([(512, 136), (550, 136)], "green")
    c.card(552, 104, 240, "arch", "network", "Internet gateway", "public subnets only")
    c.panel(48, 196, 980, 420, title="VPC java-platform-dev · 10.10.0.0/16 (prod: 10.20.0.0/16)", glyph="cloud", cat="network")
    tiers = [(244, "green", "Public subnets · 10.10.1.0/24, 10.10.2.0/24",
              [("alb", "network", "ALB · eu-west-1a", "load balancer node"), ("alb", "network", "ALB · eu-west-1b", "load balancer node")]),
             (366, "blue", "Private app subnets · 10.10.11.0/24, 10.10.12.0/24",
              [("ec2", "compute", "EC2 · eu-west-1a", "app instance"), ("ec2", "compute", "EC2 · eu-west-1b", "app instance"),
               ("folder", "storage", "EFS mount targets", "one per subnet"), ("endpoint", "network", "VPC endpoints", "1a · both AZs in prod")]),
             (488, "purple", "Private database subnets · 10.10.21.0/24, 10.10.22.0/24",
              [("db", "database", "RDS primary · 1a", "MySQL 8.4"), ("db", "database", "RDS standby · 1b", "prod only (Multi-AZ)")])]
    for y, tone, title, items in tiers:
        c.panel(64, y, 948, 110, tone, title, dashed=True)
        for j, (g, cat, a, b) in enumerate(items):
            c.small(80 + j * 232, y + 44, 220, g, cat, a, b, tone)
    c.panel(1052, 196, 400, 420, title="Reached privately (no NAT)")
    for i, (g, cat, ti, sub) in enumerate([("bucket", "storage", "S3 gateway endpoint", "artifacts, packages · free"),
                                           ("gear", "mgmt", "SSM + Session Manager", "no SSH, no bastion"),
                                           ("vault", "security", "Secrets Manager", "DB password"),
                                           ("watch", "mgmt", "CloudWatch", "logs, metrics, flow logs"),
                                           ("key", "security", "KMS", "used through AWS services")]):
        c.card(1068, 240 + i * 72, 368, g, cat, ti, sub)
    c.arrow([(1012, 420), (1050, 420)], "green")
    c.arrow([(672, 168), (672, 242)], "green", "443", 682, 222, anchor="start")
    c.panel(48, 640, 1404, 112, "orange", "Build VPC java-platform-build · 10.30.0.0/16 · no internet gateway, no NAT", dashed=True)
    for i, (g, cat, a, b) in enumerate([("ec2", "compute", "Image Builder instance", "t4g.medium, temporary"),
                                        ("endpoint", "network", "4 endpoints, one AZ", "imagebuilder, ssm, logs"),
                                        ("bucket", "storage", "S3 allow-list", "Image Builder, SSM, AL2023 repos"),
                                        ("key", "security", "Own KMS key", "encrypts its flow logs")]):
        c.small(64 + i * 316, 684, 300, g, cat, a, b, "orange")
    return c.render()


def image(theme):
    c = Canvas(theme, W, 440, "Image pipeline: EC2 Image Builder patches, installs, tests and publishes a Graviton AMI.")
    c.band(24, 24, 1452, 392, "orange", "java-ami · app AMI",
           "EC2 Image Builder bakes a patched, fully immutable image with the application release inside")
    flow = [("layers", "compute", "Parent image", "AL2023 arm64 · latest"),
            ("gear", "compute", "Build", "patch, runtime, release"),
            ("check", "compute", "Validate + test", "fresh instance, reboot"),
            ("ami", "compute", "Encrypted AMI", "java-app-<version>-arm64"),
            ("approve", "github", "Pinned by ID", "dev, then promote to prod")]
    for i, (g, cat, ti, sub) in enumerate(flow):
        x = 48 + i * 280
        c.card(x, 112, 250, g, cat, ti, sub)
        if i < 4:
            c.arrow([(x + 253, 144), (x + 277, 144)], "orange")
    c.panel(48, 204, 680, 100, title="Installed in the image")
    for i, (g, a, b) in enumerate([("doc", "Corretto 21 + agents", "CloudWatch, efs-utils"), ("box", "Release JAR", "checksum-verified"),
                                   ("gear", "systemd units", "configure + app")]):
        c.small(64 + i * 220, 240, 210, g, "compute", a, b, "orange")
    c.panel(752, 204, 700, 100, title="Versions")
    for i, (a, b) in enumerate([("app_version 0.1.0", "release baked in"), ("recipe 1.0.0", "bump every release"),
                                ("build /1, /2 …", "added per run")]):
        c.small(768 + i * 226, 240, 214, "var", "compute", a, b, "orange")
    for i, (g, cat, ti, sub) in enumerate([("play", "github", "Triggers", "merge, manual, weekly"),
                                           ("shield", "security", "Fails closed", "no AMI if a test fails"),
                                           ("layers", "compute", "Lifecycle", "newest 5 + any in use"),
                                           ("lock", "security", "Hardened build", "IMDSv2, private, encrypted")]):
        c.card(48 + i * 352, 326, 326, g, cat, ti, sub)
    return c.render()


def workload(theme):
    c = Canvas(theme, W, 596, "Application tier: request path with one security-group rule per hop, instance boot steps and observability.")
    c.band(24, 24, 1452, 548, "purple", "java-infra · application tier",
           "One request path, one security-group rule per hop, rolling releases")
    flow = [("user", "neutral", "Users", "browser, curl"), ("r53", "network", "Route 53", "alias record"),
            ("wall", "security", "AWS WAF", "prod: managed rules"), ("alb", "network", "Load balancer", "TLS 1.3 · :443"),
            ("asg", "compute", "App instances", "Auto Scaling · :8080")]
    labels = ["DNS", "HTTPS", "", "HTTP"]
    for i, (g, cat, ti, sub) in enumerate(flow):
        x = 48 + i * 234
        c.card(x, 112, 200, g, cat, ti, sub)
        if i < 4:
            c.arrow([(x + 203, 144), (x + 231, 144)], "purple")
            if labels[i]:
                c.text(x + 217, 104, labels[i], 11.5, anchor="middle", weight="600")
    data = [("db", "database", "RDS MySQL", ":3306, TLS required"), ("folder", "storage", "EFS", ":2049, TLS + IAM"),
            ("vault", "security", "Secrets Manager", ":443 via endpoint")]
    for i, (g, cat, a, b) in enumerate(data):
        y = 92 + i * 62
        c.small(1218, y, 234, g, cat, a, b, "purple")
        c.arrow([(1184, 144), (1200, 144), (1200, y + 26), (1216, y + 26)], "purple")
    c.text(48, 284, "Security groups: alb ← internet 80/443 · app ← alb 8080 · db ← app 3306 · efs ← app 2049 · endpoints ← VPC 443", 13)
    c.panel(48, 304, 1404, 150, title="Every new instance (no user data: logic baked into the AMI)")
    steps = [("ec2", "1 Boot app AMI", "release already inside"), ("token", "2 Read tag", "Environment via IMDSv2"),
             ("gear", "3 Load settings", "SSM /<env>/app/*"), ("folder", "4 Mount EFS", "TLS, IAM, access point"),
             ("play", "5 Start app", "systemd, CW agent"), ("check", "6 In service", "/health = 200")]
    for i, (g, a, b) in enumerate(steps):
        c.small(64 + i * 224, 344, 212, g, "compute", a, b, "purple")
    c.text(64, 428, "Rolling instance refresh: new instances must pass /health before old ones leave; auto-rollback if they never do.", 13)
    for i, (g, cat, ti, sub) in enumerate([("watch", "mgmt", "CloudWatch Logs", "app, RDS, WAF, flow"),
                                           ("mail", "mgmt", "Alarms → SNS", "5xx, health, latency, DB"),
                                           ("bucket", "storage", "ALB access logs", "S3, lifecycle"),
                                           ("db", "database", "Backups", "14 days + final snapshot"),
                                           ("key", "security", "KMS everywhere", "EBS, RDS, EFS, logs")]):
        c.card(48 + i * 283, 480, 270, g, cat, ti, sub)
    return c.render()


def delivery(theme):
    c = Canvas(theme, W, 470, "Delivery: pull requests run checks and read-only plans; merging applies dev, then prod after approval.")
    c.band(24, 24, 1452, 200, "gray", "Pull request", "Checks and read-only plans; ci is the only required status")
    pr = [("play", "github", "Static checks", "fmt, validate, tflint, Trivy"),
          ("search", "neutral", "Detect changes", "skip plans for docs"),
          ("terraform", "network", "Plan (read-only)", "*-plan role, in summary"),
          ("check", "github", "ci", "required on main"),
          ("approve", "github", "Review + merge", "squash into main")]
    for i, (g, cat, ti, sub) in enumerate(pr):
        x = 48 + i * 277
        c.card(x, 110, 244, g, cat, ti, sub)
        if i < 4:
            c.arrow([(x + 247, 142), (x + 274, 142)], "gray")
    c.arrow([(750, 224), (750, 248)], "gray")
    c.band(24, 250, 1452, 196, "blue", "Merge to main → deploy.yml",
           "Applies in order; production waits for an approval and applies exactly the reviewed plan")
    dp = [("play", "github", "Apply shared", "platform-infra only"),
          ("play", "github", "Apply dev", "development role"),
          ("doc", "network", "Plan prod", "saved, not applied"),
          ("approve", "github", "Approval", "required reviewer"),
          ("check", "github", "Apply prod", "the exact saved plan")]
    for i, (g, cat, ti, sub) in enumerate(dp):
        x = 48 + i * 277
        c.card(x, 336, 244, g, cat, ti, sub)
        if i < 4:
            c.arrow([(x + 247, 368), (x + 274, 368)], "blue")
    c.text(1452, 430, "Prod steps run only when PRODUCTION_ENABLED = true", 12.5, anchor="end")
    return c.render()


ALL = {"overview": overview, "identity": identity, "network": network,
       "image-pipeline": image, "workload": workload, "delivery": delivery}
