# Lightweight Association Storage for Memory Consolidation

## Overview

This document describes how to implement association storage within the existing memory system, without adding graph database complexity. Associations discovered during the dream-inspired consolidation process become first-class memories themselves, creating an elegant and recursive system.

> **Note**: This approach provides graph-like capabilities while maintaining the simplicity of the existing vector storage system.

## Core Concept

Instead of adding a separate graph database, we store associations as special memories with rich metadata. This approach aligns perfectly with the dream-inspired consolidation system, where creative associations are already being discovered.

```python
# Associations are memories too!
association_memory = Memory(
    content="Description of the discovered connection",
    metadata={
        "type": "association",
        "source_hash": memory1.hash,
        "target_hash": memory2.hash,
        "similarity_score": 0.54,
        "insight": "Both memories relate to optimization patterns"
    },
    tags=["association", "discovery", "creative"]
)
```

## Implementation

### Enhanced Creative Association Engine

```python
from datetime import datetime
from typing import List, Tuple, Dict
import numpy as np

class EnhancedCreativeAssociationEngine:
    """
    Stores discovered associations as first-class memories in the system.
    No graph database needed - associations ARE memories!
    """
    
    def __init__(self, storage):
        self.storage = storage
        self.min_similarity = 0.3
        self.max_similarity = 0.7
    
    async def creative_association_phase(
        self, 
        memories: List[Memory], 
        time_horizon: str
    ) -> List[Memory]:
        """
        Discover creative associations and store them as memories.
        
        This is the heart of the dream-inspired system - finding
        non-obvious connections in the "sweet spot" of similarity.
        """
        associations_discovered = []
        
        # Sample memory pairs to avoid combinatorial explosion
        pairs = self._sample_memory_pairs(memories, max_pairs=100)
        
        for mem1, mem2 in pairs:
            # Calculate semantic similarity using existing embeddings
            similarity = self._calculate_similarity(mem1, mem2)
            
            # Check if in the creative sweet spot
            if self.min_similarity < similarity < self.max_similarity:
                # Create association memory
                association = await self._create_association_memory(
                    mem1, mem2, similarity, time_horizon
                )
                
                # Store it like any other memory!
                success = await self.storage.store(association)
                if success:
                    associations_discovered.append(association)
                    
                    # Update original memories' metadata
                    await self._update_memory_connections(mem1, mem2, association)
        
        return associations_discovered
    
    async def _create_association_memory(
        self, 
        mem1: Memory, 
        mem2: Memory, 
        similarity: float, 
        time_horizon: str
    ) -> Memory:
        """
        Create a rich association memory that captures the insight.
        """
        # Analyze why these memories might be connected
        insight = self._analyze_connection(mem1, mem2, similarity)
        connection_type = self._classify_connection(similarity)
        
        # Create human-readable content
        content = f"""
Creative Association Discovered ({connection_type}):

Memory 1: "{mem1.content[:100]}..."
Memory 2: "{mem2.content[:100]}..."

Connection Strength: {similarity:.2f}
Discovered During: {time_horizon} consolidation

Insight: {insight}

This association reveals a {connection_type} connection between concepts 
that may not be immediately obvious but could provide valuable insights.
        """.strip()
        
        # Rich metadata for querying
        metadata = {
            "type": "association",
            "subtype": "creative_discovery",
            "source_hash": mem1.hash,
            "target_hash": mem2.hash,
            "source_preview": mem1.content[:50],
            "target_preview": mem2.content[:50],
            "similarity_score": similarity,
            "connection_type": connection_type,
            "discovered_during": f"{time_horizon}_consolidation",
            "discovery_timestamp": datetime.now().isoformat(),
            "insight": insight,
            "memory_types": [mem1.memory_type, mem2.memory_type],
            "common_tags": list(set(mem1.tags) & set(mem2.tags)),
            "combined_importance": (mem1.importance_score + mem2.importance_score) / 2
        }
        
        # Tags for easy filtering
        tags = [
            "association",
            "discovery",
            connection_type,
            time_horizon,
            "creative"
        ]
        tags.extend(metadata['common_tags'])
        
        return Memory(
            content=content,
            metadata=metadata,
            tags=tags,
            memory_type="association",
            importance_score=similarity * metadata['combined_importance']
        )
    
    def _analyze_connection(self, mem1: Memory, mem2: Memory, similarity: float) -> str:
        """
        Generate insight about why these memories might be connected.
        In the full implementation, this could use an SLM for richer insights.
        """
        common_tags = set(mem1.tags) & set(mem2.tags)
        
        if common_tags:
            return f"Share common themes: {', '.join(common_tags)}"
        elif similarity > 0.5:
            return "Strong conceptual similarity despite different contexts"
        elif similarity < 0.4:
            return "Unexpected connection revealing hidden pattern"
        else:
            return "Moderate connection suggesting complementary concepts"
    
    def _classify_connection(self, similarity: float) -> str:
        """Classify the type of creative connection."""
        if similarity > 0.6:
            return "strong-conceptual"
        elif similarity > 0.5:
            return "moderate-thematic"
        elif similarity > 0.4:
            return "subtle-pattern"
        else:
            return "creative-leap"
    
    def _calculate_similarity(self, mem1: Memory, mem2: Memory) -> float:
        """Calculate cosine similarity between memory embeddings."""
        vec1 = np.array(mem1.embedding)
        vec2 = np.array(mem2.embedding)
        
        dot_product = np.dot(vec1, vec2)
        norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        
        return float(dot_product / norm_product) if norm_product > 0 else 0.0
    
    def _sample_memory_pairs(
        self, 
        memories: List[Memory], 
        max_pairs: int = 100
    ) -> List[Tuple[Memory, Memory]]:
        """
        Intelligently sample memory pairs for association discovery.
        """
        if len(memories) < 2:
            return []
        
        # For small sets, check all pairs
        if len(memories) * (len(memories) - 1) / 2 <= max_pairs:
            from itertools import combinations
            return list(combinations(memories, 2))
        
        # For large sets, use importance-weighted sampling
        weights = np.array([m.importance_score for m in memories])
        weights = weights / weights.sum()
        
        pairs = set()
        attempts = 0
        while len(pairs) < max_pairs and attempts < max_pairs * 3:
            # Sample two different memories
            indices = np.random.choice(
                len(memories), 
                size=2, 
                replace=False, 
                p=weights
            )
            pair = tuple(sorted([memories[indices[0]].hash, memories[indices[1]].hash]))
            
            if pair not in pairs:
                pairs.add(pair)
                
            attempts += 1
        
        # Convert back to memory pairs
        hash_to_memory = {m.hash: m for m in memories}
        return [(hash_to_memory[h1], hash_to_memory[h2]) for h1, h2 in pairs]
```

### Association Explorer

```python
class AssociationExplorer:
    """
    Explore connections between memories through associations.
    No graph database needed - just smart queries!
    """
    
    def __init__(self, storage):
        self.storage = storage
    
    async def find_connection_path(
        self, 
        start_hash: str, 
        end_hash: str, 
        max_depth: int = 3
    ) -> List[List[Dict]]:
        """
        Find how two memories connect through associations.
        Returns all paths up to max_depth.
        """
        visited = set()
        all_paths = []
        
        async def explore(current_hash: str, path: List[Dict], depth: int):
            if depth > max_depth or current_hash in visited:
                return
                
            visited.add(current_hash)
            
            # Find associations involving this memory
            associations = await self.storage.search(
                query="",  # Empty query, use filter only
                filter={
                    "$or": [
                        {"source_hash": current_hash},
                        {"target_hash": current_hash}
                    ],
                    "type": "association"
                },
                n_results=20
            )
            
            for assoc in associations:
                # Determine the other memory in this association
                other_hash = (
                    assoc.metadata['target_hash'] 
                    if assoc.metadata['source_hash'] == current_hash 
                    else assoc.metadata['source_hash']
                )
                
                # Build path segment
                segment = {
                    'from': current_hash,
                    'to': other_hash,
                    'association': assoc.hash,
                    'strength': assoc.metadata.get('similarity_score', 0),
                    'type': assoc.metadata.get('connection_type', 'unknown'),
                    'insight': assoc.metadata.get('insight', '')
                }
                
                new_path = path + [segment]
                
                if other_hash == end_hash:
                    # Found a complete path!
                    all_paths.append(new_path)
                else:
                    # Continue exploring
                    await explore(other_hash, new_path, depth + 1)
        
        await explore(start_hash, [], 0)
        return all_paths
    
    async def get_memory_connections(
        self, 
        memory_hash: str, 
        connection_types: List[str] = None
    ) -> Dict:
        """
        Get all connections for a memory, organized by type.
        """
        # Find all associations
        associations = await self.storage.search(
            query="",
            filter={
                "$or": [
                    {"source_hash": memory_hash},
                    {"target_hash": memory_hash}
                ],
                "type": "association"
            },
            n_results=50
        )
        
        # Filter by connection type if specified
        if connection_types:
            associations = [
                a for a in associations 
                if a.metadata.get('connection_type') in connection_types
            ]
        
        # Organize by connection type
        connections_by_type = {}
        for assoc in associations:
            conn_type = assoc.metadata.get('connection_type', 'unknown')
            if conn_type not in connections_by_type:
                connections_by_type[conn_type] = []
            
            # Determine which memory is the "other" one
            is_source = assoc.metadata['source_hash'] == memory_hash
            other_hash = (
                assoc.metadata['target_hash'] if is_source 
                else assoc.metadata['source_hash']
            )
            
            connections_by_type[conn_type].append({
                'memory_hash': other_hash,
                'memory_preview': (
                    assoc.metadata['target_preview'] if is_source 
                    else assoc.metadata['source_preview']
                ),
                'strength': assoc.metadata.get('similarity_score', 0),
                'insight': assoc.metadata.get('insight', ''),
                'discovered': assoc.metadata.get('discovery_timestamp', ''),
                'association_hash': assoc.hash
            })
        
        # Sort each type by strength
        for conn_type in connections_by_type:
            connections_by_type[conn_type].sort(
                key=lambda x: x['strength'], 
                reverse=True
            )
        
        return connections_by_type
    
    async def find_memory_clusters(self, min_connections: int = 3) -> List[Set[str]]:
        """
        Find clusters of highly interconnected memories.
        Simple approach without graph algorithms.
        """
        # Get all recent associations
        recent_associations = await self.storage.search(
            query="",
            filter={
                "type": "association",
                "created_at": {
                    "$gte": (datetime.now() - timedelta(days=30)).timestamp()
                }
            },
            n_results=1000
        )
        
        # Build adjacency map
        connections = {}
        for assoc in recent_associations:
            source = assoc.metadata['source_hash']
            target = assoc.metadata['target_hash']
            
            if source not in connections:
                connections[source] = set()
            if target not in connections:
                connections[target] = set()
                
            connections[source].add(target)
            connections[target].add(source)
        
        # Find clusters (simple connected components)
        visited = set()
        clusters = []
        
        for memory_hash in connections:
            if memory_hash in visited:
                continue
                
            # BFS to find connected component
            cluster = set()
            queue = [memory_hash]
            
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                    
                visited.add(current)
                cluster.add(current)
                
                # Add unvisited neighbors
                for neighbor in connections.get(current, []):
                    if neighbor not in visited:
                        queue.append(neighbor)
            
            # Only keep significant clusters
            if len(cluster) >= min_connections:
                clusters.append(cluster)
        
        return sorted(clusters, key=len, reverse=True)
```

### Meta-Association Discovery

```python
class MetaAssociationEngine:
    """
    Discover patterns in associations themselves!
    This creates emergent, higher-order insights.
    """
    
    async def discover_meta_patterns(self, time_window: timedelta = timedelta(days=7)):
        """
        Find patterns in recent associations.
        """
        # Get recent associations
        recent = await self.storage.search(
            query="",
            filter={
                "type": "association",
                "created_at": {
                    "$gte": (datetime.now() - time_window).timestamp()
                }
            },
            n_results=100
        )
        
        meta_associations = []
        
        # Look for convergence patterns
        convergence_points = {}
        for assoc in recent:
            for memory_hash in [assoc.metadata['source_hash'], 
                               assoc.metadata['target_hash']]:
                if memory_hash not in convergence_points:
                    convergence_points[memory_hash] = []
                convergence_points[memory_hash].append(assoc)
        
        # Create meta-associations for convergence points
        for memory_hash, associations in convergence_points.items():
            if len(associations) >= 3:  # Significant convergence
                meta = await self._create_convergence_association(
                    memory_hash, 
                    associations
                )
                meta_associations.append(meta)
        
        # Look for association chains
        chains = await self._find_association_chains(recent)
        for chain in chains:
            meta = await self._create_chain_association(chain)
            meta_associations.append(meta)
        
        # Store all meta-associations
        for meta in meta_associations:
            await self.storage.store(meta)
        
        return meta_associations
    
    async def _create_convergence_association(
        self, 
        convergence_point: str, 
        associations: List[Memory]
    ) -> Memory:
        """
        Create a meta-association for a convergence pattern.
        """
        # Get the actual memory that's the convergence point
        memory = await self.storage.get_by_hash(convergence_point)
        
        content = f"""
Meta-Pattern: Convergence Point Discovered

Central Memory: "{memory.content[:100]}..."

This memory has become a convergence point with {len(associations)} creative 
associations discovered in recent consolidations. This suggests it may be a 
key concept or bridge between different knowledge domains.

Connected Concepts:
"""
        
        for assoc in associations[:5]:  # Top 5
            other_preview = (
                assoc.metadata['target_preview'] 
                if assoc.metadata['source_hash'] == convergence_point
                else assoc.metadata['source_preview']
            )
            content += f"\n- {other_preview} (strength: {assoc.metadata.get('similarity_score', 0):.2f})"
        
        return Memory(
            content=content,
            metadata={
                "type": "association",
                "subtype": "meta_pattern",
                "pattern_type": "convergence",
                "convergence_point": convergence_point,
                "association_count": len(associations),
                "association_hashes": [a.hash for a in associations],
                "discovered_at": datetime.now().isoformat()
            },
            tags=["meta-association", "convergence", "pattern", "emergent"],
            memory_type="meta_association",
            importance_score=0.8 + (0.02 * len(associations))  # Higher importance
        )
```

## Integration with Dream-Inspired Consolidation

```python
class AssociationAwareConsolidator(DreamInspiredConsolidator):
    """
    Enhanced consolidator that treats associations as first-class memories.
    """
    
    def __init__(self, storage, config):
        super().__init__(storage, config)
        self.association_engine = EnhancedCreativeAssociationEngine(storage)
        self.explorer = AssociationExplorer(storage)
        self.meta_engine = MetaAssociationEngine(storage)
    
    async def consolidate(self, time_horizon: str):
        """
        Full consolidation pipeline with association storage.
        """
        # 1. Get memories for this time horizon
        memories = await self.storage.get_memories_for_horizon(time_horizon)
        
        # 2. Update relevance scores (including associations!)
        await self.update_relevance_scores(memories)
        
        # 3. Discover and store new associations
        new_associations = await self.association_engine.creative_association_phase(
            memories, 
            time_horizon
        )
        
        # 4. Include associations in clustering
        # Associations can be clustered with regular memories!
        all_memories = memories + new_associations
        clusters = await self.cluster_memories(all_memories)
        
        # 5. Compress clusters (associations included)
        compressed = await self.compress_clusters(clusters)
        
        # 6. Discover meta-patterns (monthly and above)
        meta_associations = []
        if time_horizon in ['monthly', 'quarterly', 'yearly']:
            meta_associations = await self.meta_engine.discover_meta_patterns()
        
        # 7. Find emerging knowledge structures
        knowledge_clusters = await self.explorer.find_memory_clusters()
        
        return {
            'memories_processed': len(memories),
            'associations_discovered': len(new_associations),
            'meta_patterns_found': len(meta_associations),
            'clusters_formed': len(clusters),
            'knowledge_structures': len(knowledge_clusters),
            'compressed_summaries': len(compressed)
        }
```

## Benefits of This Approach

### 1. **Zero Additional Complexity**
- No new database systems
- No synchronization issues
- Uses existing storage and search

### 2. **Associations as Knowledge**
- Associations are searchable: "Find all creative connections from last month"
- Associations can be tagged and categorized
- Associations have their own importance scores

### 3. **Recursive Insights**
- Associations can have associations
- Meta-patterns emerge naturally
- Knowledge structures self-organize

### 4. **Temporal Awareness**
- Know when connections were discovered
- Track how associations evolve
- See which consolidation cycles were most insightful

### 5. **Natural Integration**
- Associations participate in consolidation
- Old associations can decay or be reinforced
- Important associations bubble up through PageRank-like importance

## Query Examples

```python
# Find all creative connections discovered this week
associations = await storage.search(
    query="creative association discovered",
    filter={
        "type": "association",
        "created_at": {"$gte": week_ago_timestamp}
    }
)

# Find how two concepts connect
paths = await explorer.find_connection_path(
    "memory_hash_1", 
    "memory_hash_2",
    max_depth=3
)

# Get all connections for a specific memory
connections = await explorer.get_memory_connections(
    "memory_hash",
    connection_types=["creative-leap", "strong-conceptual"]
)

# Find convergence points (highly connected memories)
meta_patterns = await storage.search(
    query="convergence point",
    filter={
        "type": "association",
        "subtype": "meta_pattern",
        "pattern_type": "convergence"
    }
)
```

## Future Enhancements

1. **Association Strength Decay** - Associations can weaken over time if not reinforced
2. **Association Reinforcement** - Repeated discovery strengthens associations
3. **Negative Associations** - Store "contradicts" or "replaces" relationships
4. **Association Chains** - Discover multi-hop insight paths
5. **Visualization Export** - Generate data for external graph visualization

## Conclusion

By treating associations as first-class memories, we achieve graph-like capabilities without the complexity of a graph database. This approach:

- Maintains system simplicity
- Provides rich relationship tracking
- Enables emergent pattern discovery
- Scales naturally with the existing system
- Stays true to the biological inspiration

The associations become part of the living memory system, growing and evolving just like regular memories. They can decay, be reinforced, get consolidated, and even form their own associations. This recursive approach creates a truly organic knowledge management system.

---

**Related Documents:**
- [Dream-Inspired Memory Consolidation](./dream-inspired-memory-consolidation.md)
- [Autonomous Memory Consolidation](./autonomous-memory-consolidation.md)
- [Hybrid SLM Memory Consolidation](./hybrid-slm-memory-consolidation.md)

*Created: July 28, 2025*