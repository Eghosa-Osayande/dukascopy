class InstrumentGroup {
  final String id;
  final String title;
  final String? parent;
  final List<String> instruments;

  InstrumentGroup({
    required this.id,
    required this.title,
    this.parent,
    required this.instruments,
  });

  factory InstrumentGroup.fromJson(Map<String, dynamic> json) {
    return InstrumentGroup(
      id: json['id'] as String,
      title: json['title'] as String,
      parent: json['parent'] as String?,



      instruments:
          (json['instruments'] as List<dynamic>? ?? <dynamic>[]).cast<String>(),
    );
  }
}


